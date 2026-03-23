from pydantic import BaseModel, Field
from typing import Literal


class SubmitTextRequest(BaseModel):
    text: str = Field(..., max_length=5000)


class SessionResponse(BaseModel):
    session_id: str


class Source(BaseModel):
    title: str
    url: str
    snippet: str
    nli_verdict: Literal["supports", "contradicts", "neutral"]
    nli_score: float


class ClaimResult(BaseModel):
    index: int
    claim: str
    verdict: Literal["supports", "contradicts", "neutral"]
    confidence: float
    sources: list[Source]
