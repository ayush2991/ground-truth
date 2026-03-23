"""Unit tests for web search."""

import sys
import os
import asyncio
from unittest.mock import AsyncMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.pipeline import searcher


async def test_search_mock():
    """Test search with mocked API response."""
    # Mock the httpx.AsyncClient
    mock_response = {
        "web": {
            "results": [
                {
                    "title": "Earth Age - NASA",
                    "url": "https://nasa.gov/earth-age",
                    "description": "The Earth is approximately 4.5 billion years old.",
                    "extra_snippets": ["This is based on geological evidence.", "Radiometric dating confirms this."],
                },
                {
                    "title": "How Old is Earth?",
                    "url": "https://usgs.gov/earth-age",
                    "description": "Scientists estimate the age of Earth to be 4.54 billion years.",
                    "extra_snippets": [],
                },
            ]
        }
    }

    with patch("app.pipeline.searcher.httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.get.return_value = AsyncMock(json=lambda: mock_response)
        mock_client.return_value = mock_instance

        # Set BRAVE_API_KEY for the test
        with patch.dict(os.environ, {"BRAVE_API_KEY": "test-key"}):
            results = await searcher.search("earth age", count=5)

    # Verify results
    assert isinstance(results, list)
    assert len(results) == 2

    # Check first result
    assert results[0]["title"] == "Earth Age - NASA"
    assert results[0]["url"] == "https://nasa.gov/earth-age"
    assert "4.5 billion" in results[0]["snippet"]
    assert "geological evidence" in results[0]["snippet"]

    # Check second result
    assert results[1]["title"] == "How Old is Earth?"
    assert results[1]["url"] == "https://usgs.gov/earth-age"
    assert "4.54 billion" in results[1]["snippet"]

    print("✓ Search mock test passed:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result['title']}")
        print(f"     URL: {result['url']}")
        print(f"     Snippet: {result['snippet'][:80]}...")


async def test_search_empty():
    """Test search with no results."""
    mock_response = {"web": {"results": []}}

    with patch("app.pipeline.searcher.httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.get.return_value = AsyncMock(json=lambda: mock_response)
        mock_client.return_value = mock_instance

        with patch.dict(os.environ, {"BRAVE_API_KEY": "test-key"}):
            results = await searcher.search("asdfjkl;", count=5)

    assert isinstance(results, list)
    assert len(results) == 0
    print("\n✓ Empty results test passed")


if __name__ == "__main__":
    asyncio.run(test_search_mock())
    asyncio.run(test_search_empty())
    print("\n✓ All searcher tests passed!")
