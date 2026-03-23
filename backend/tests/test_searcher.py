"""Unit tests for web search."""

import sys
import os
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.pipeline import searcher


def test_build_query_no_pronoun():
    """Query without a pronoun is returned unchanged."""
    result = searcher._build_query("The Earth is 4.5 billion years old.", "Some context.")
    assert result == "The Earth is 4.5 billion years old."
    print("✓ Non-pronoun query unchanged")


def test_build_query_pronoun_resolved():
    """Pronoun at start of claim is replaced with the most common proper noun."""
    original = "Project Hail Mary is a movie. It has a 100% rating on Rotten Tomatoes."
    result = searcher._build_query("It has a 100% rating on Rotten Tomatoes.", original)
    assert "Project Hail Mary" in result
    assert result.startswith("Project Hail Mary")
    print(f"✓ Pronoun resolved: {result!r}")


def test_build_query_pronoun_no_context():
    """Pronoun without original_text falls back to the raw claim."""
    result = searcher._build_query("It is the highest grossing movie.", "")
    assert result == "It is the highest grossing movie."
    print("✓ Pronoun with no context returns raw claim")


async def test_search_mock():
    """Test search with mocked Tavily client."""
    mock_response = {
        "results": [
            {
                "title": "Earth Age - NASA",
                "url": "https://nasa.gov/earth-age",
                "content": "The Earth is approximately 4.5 billion years old based on radiometric dating of rocks and meteorites.",
            },
            {
                "title": "How Old is Earth?",
                "url": "https://usgs.gov/earth-age",
                "content": "Scientists estimate the age of Earth to be 4.54 billion years using uranium-lead dating.",
            },
        ]
    }

    mock_client = AsyncMock()
    mock_client.search.return_value = mock_response

    with patch("app.pipeline.searcher.AsyncTavilyClient", return_value=mock_client):
        with patch.dict(os.environ, {"TAVILY_API_KEY": "test-key"}):
            results = await searcher.search("earth age", count=5)

    assert isinstance(results, list)
    assert len(results) == 2
    assert results[0]["title"] == "Earth Age - NASA"
    assert results[0]["url"] == "https://nasa.gov/earth-age"
    assert "4.5 billion" in results[0]["snippet"]
    assert results[1]["title"] == "How Old is Earth?"

    print("✓ Search mock test passed:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result['title']}")
        print(f"     URL: {result['url']}")
        print(f"     Snippet: {result['snippet'][:80]}...")


async def test_search_uses_advanced_depth():
    """search() calls Tavily with search_depth='advanced'."""
    mock_client = AsyncMock()
    mock_client.search.return_value = {"results": []}

    with patch("app.pipeline.searcher.AsyncTavilyClient", return_value=mock_client):
        with patch.dict(os.environ, {"TAVILY_API_KEY": "test-key"}):
            await searcher.search("some claim", count=3)

    call_kwargs = mock_client.search.call_args.kwargs
    assert call_kwargs.get("search_depth") == "advanced"
    assert call_kwargs.get("max_results") == 3
    print("✓ Tavily called with search_depth='advanced'")


async def test_search_empty():
    """Test search with no results."""
    mock_client = AsyncMock()
    mock_client.search.return_value = {"results": []}

    with patch("app.pipeline.searcher.AsyncTavilyClient", return_value=mock_client):
        with patch.dict(os.environ, {"TAVILY_API_KEY": "test-key"}):
            results = await searcher.search("asdfjkl;", count=5)

    assert isinstance(results, list)
    assert len(results) == 0
    print("\n✓ Empty results test passed")


if __name__ == "__main__":
    test_build_query_no_pronoun()
    test_build_query_pronoun_resolved()
    test_build_query_pronoun_no_context()
    asyncio.run(test_search_mock())
    asyncio.run(test_search_uses_advanced_depth())
    asyncio.run(test_search_empty())
    print("\n✓ All searcher tests passed!")
