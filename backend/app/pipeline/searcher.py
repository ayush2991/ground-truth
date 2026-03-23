"""Web search module using Brave Search API."""

import os
import httpx
import json

BASE_URL = "https://api.search.brave.com/res/v1/web/search"


async def search(query: str, count: int = 5) -> list[dict]:
    """
    Search the web using Brave Search API.

    Args:
        query: The search query
        count: Number of results to return (default 5)

    Returns:
        A list of dicts with keys: title, url, snippet
    """
    api_key = os.getenv("BRAVE_API_KEY")
    if not api_key:
        raise ValueError("BRAVE_API_KEY environment variable not set")

    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": api_key,
    }

    params = {
        "q": query,
        "count": count,
        "extra_snippets": "true",  # Get additional snippet excerpts
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()

    data = response.json()
    results = data.get("web", {}).get("results", [])

    # Parse results
    parsed_results = []
    for result in results:
        # Combine description with extra snippets for richer context
        snippet_parts = [result.get("description", "")]
        extra_snippets = result.get("extra_snippets", [])
        if extra_snippets:
            snippet_parts.extend(extra_snippets[:2])  # Take up to 2 extra snippets
        snippet = " ".join(p for p in snippet_parts if p)

        parsed_results.append({
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "snippet": snippet,
        })

    return parsed_results
