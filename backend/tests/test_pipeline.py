"""Integration test for the full fact-checking pipeline."""

import sys
import os
import asyncio
import json
from unittest.mock import AsyncMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.routes import factcheck


async def test_pipeline_full():
    """Test the full pipeline with mocked search."""
    # Tavily-style results: content field holds clean page extracts
    mock_search_results = [
        {
            "title": "NASA - Earth Age",
            "url": "https://nasa.gov/earth-age",
            "snippet": (
                "The Earth is approximately 4.5 billion years old. "
                "This age is determined through radiometric dating of rocks and meteorites. "
                "Scientists have confirmed this estimate using multiple independent methods."
            ),
        },
        {
            "title": "USGS - Earth History",
            "url": "https://usgs.gov/earth",
            "snippet": (
                "Scientists estimate the age of Earth to be 4.54 billion years. "
                "Uranium-lead dating of ancient zircon crystals provides the most precise measurements. "
                "The oldest known rocks on Earth date back around 4 billion years."
            ),
        },
    ]

    async def mock_search(query, count=5, original_text=""):
        return mock_search_results

    # Load models
    from app.pipeline import extractor, nli
    extractor.load()
    nli.load()

    # Create a session
    import time
    test_text = "The Earth is 4.5 billion years old."
    factcheck._sessions["test-session"] = {
        "text": test_text,
        "timestamp": time.time(),
    }

    with patch("app.routes.factcheck.searcher.search", side_effect=mock_search):
        events = []
        async for event_data in factcheck._factcheck_generator("test-session"):
            events.append(event_data)

    # Verify event structure
    assert len(events) > 0

    event_names = [e["event"] for e in events]
    assert "claims_found" in event_names
    assert "claim_result" in event_names
    assert "done" in event_names

    # Check claims_found
    claims_event = next(e for e in events if e["event"] == "claims_found")
    claims_data = json.loads(claims_event["data"])
    assert claims_data["total"] >= 1
    assert len(claims_data["claims"]) >= 1

    # Check claim_result
    claim_results = [e for e in events if e["event"] == "claim_result"]
    assert len(claim_results) >= 1

    claim_result_data = json.loads(claim_results[0]["data"])
    assert "claim" in claim_result_data
    assert "verdict" in claim_result_data
    assert claim_result_data["verdict"] in ["supports", "contradicts", "neutral"]
    assert "confidence" in claim_result_data
    assert isinstance(claim_result_data["confidence"], float)
    assert 0 <= claim_result_data["confidence"] <= 1
    assert "sources" in claim_result_data
    assert len(claim_result_data["sources"]) > 0

    # Check source structure
    first_source = claim_result_data["sources"][0]
    assert "title" in first_source
    assert "url" in first_source
    assert "snippet" in first_source
    assert "nli_verdict" in first_source
    assert first_source["nli_verdict"] in ["supports", "contradicts", "neutral"]
    assert "nli_score" in first_source

    print("✓ Full pipeline test passed!")
    print(f"  Claims found: {claims_data['total']}")
    print(f"  First claim verdict: {claim_result_data['verdict']} (confidence: {claim_result_data['confidence']})")
    print(f"  Sources used: {len(claim_result_data['sources'])}")


if __name__ == "__main__":
    asyncio.run(test_pipeline_full())
    print("\n✓ All pipeline tests passed!")
