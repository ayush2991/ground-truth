import uuid
import time
import json
import asyncio
from fastapi import APIRouter, HTTPException, Query
from sse_starlette.sse import EventSourceResponse
from app.models import SubmitTextRequest, SessionResponse, Source, ClaimResult
from app.pipeline import extractor, searcher, nli, aggregator, ranker

router = APIRouter()

# In-memory session store: {session_id: {text, timestamp}}
_sessions: dict[str, dict] = {}
SESSION_TTL_SECONDS = 300  # 5 minutes


def _cleanup_expired_sessions():
    """Remove expired sessions."""
    now = time.time()
    expired = [sid for sid, data in _sessions.items() if now - data["timestamp"] > SESSION_TTL_SECONDS]
    for sid in expired:
        del _sessions[sid]


@router.post("/session")
def create_session(request: SubmitTextRequest) -> SessionResponse:
    """Create a session and store the text temporarily."""
    _cleanup_expired_sessions()

    if len(request.text) > 5000:
        raise HTTPException(status_code=422, detail="Text exceeds 5000 character limit.")

    session_id = str(uuid.uuid4())
    _sessions[session_id] = {
        "text": request.text,
        "timestamp": time.time(),
    }
    return SessionResponse(session_id=session_id)


async def _factcheck_generator(session_id: str):
    """Generator that yields SSE events for fact-checking a session."""
    # Retrieve session
    _cleanup_expired_sessions()
    if session_id not in _sessions:
        yield {
            "event": "error",
            "data": json.dumps({"message": "Session not found or expired."})
        }
        return

    text = _sessions[session_id]["text"]

    try:
        # Stage 1: Extract claims
        claims = extractor.extract(text)
        yield {
            "event": "claims_found",
            "data": json.dumps({"total": len(claims), "claims": claims})
        }

        # Stage 2-4: For each claim, search → NLI → aggregate → yield result
        for claim_idx, claim in enumerate(claims):
            try:
                # Search for evidence (pass original text for pronoun resolution)
                search_results = await searcher.search(claim, count=5, original_text=text)

                # Score each result with NLI
                nli_scores = []
                sources = []

                for result in search_results:
                    # Extract the most claim-relevant sentences from Tavily's page content
                    premise = ranker.top_sentences(result["snippet"], claim, k=3)

                    # Score premise vs hypothesis (claim)
                    scores = await asyncio.to_thread(
                        nli.score,
                        premise,
                        claim
                    )
                    nli_scores.append(scores)

                    best_verdict = max(scores, key=scores.get)
                    sources.append(Source(
                        title=result["title"],
                        url=result["url"],
                        snippet=result["snippet"],
                        nli_verdict=best_verdict,
                        nli_score=round(scores[best_verdict], 3)
                    ))

                # Aggregate verdicts
                agg_result = aggregator.aggregate(nli_scores)

                # Yield claim result
                yield {
                    "event": "claim_result",
                    "data": json.dumps({
                        "index": claim_idx,
                        "claim": claim,
                        "verdict": agg_result["verdict"],
                        "confidence": agg_result["confidence"],
                        "sources": [s.model_dump() for s in sources]
                    })
                }

            except Exception as claim_error:
                # Yield error for this claim but continue with others
                yield {
                    "event": "claim_result",
                    "data": json.dumps({
                        "index": claim_idx,
                        "claim": claim,
                        "verdict": "neutral",
                        "confidence": 0.0,
                        "sources": [],
                        "error": str(claim_error)
                    })
                }

        # Done
        yield {
            "event": "done",
            "data": json.dumps({})
        }

    except Exception as e:
        yield {
            "event": "error",
            "data": json.dumps({"message": str(e)})
        }


@router.get("/factcheck/stream")
async def factcheck_stream(session_id: str = Query(...)) -> EventSourceResponse:
    """Stream fact-checking results as Server-Sent Events."""
    return EventSourceResponse(_factcheck_generator(session_id))
