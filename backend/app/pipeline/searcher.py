"""Web search module using Tavily Search API."""

import os
import re
from collections import Counter
from tavily import AsyncTavilyClient

_PRONOUNS = {"it", "he", "she", "they", "this", "that", "these", "those", "its", "their"}


def _build_query(claim: str, original_text: str) -> str:
    """
    Build a focused search query from a claim.

    If the claim starts with a pronoun, attempt to resolve the subject using
    capitalized proper nouns found in the original text.
    """
    first_word = claim.split()[0].lower() if claim.split() else ""
    if first_word not in _PRONOUNS or not original_text:
        return claim

    # Extract proper noun phrases (sequences of capitalized words)
    proper_nouns = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", original_text)
    if not proper_nouns:
        return claim

    subject = Counter(proper_nouns).most_common(1)[0][0]
    return f"{subject} {claim}"


async def search(query: str, count: int = 5, original_text: str = "") -> list[dict]:
    """
    Search the web using Tavily Search API and return clean page extracts.

    Args:
        query: The claim or search query
        count: Number of results to return (default 5)
        original_text: Full original input text, used for pronoun resolution

    Returns:
        A list of dicts with keys: title, url, snippet
        where snippet is Tavily's clean page content extract (not a meta-description).
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY environment variable not set")

    enriched_query = _build_query(query, original_text)

    client = AsyncTavilyClient(api_key=api_key)
    response = await client.search(
        query=enriched_query,
        max_results=count,
        search_depth="advanced",  # Extracts actual page content, not just meta
    )

    results = response.get("results", [])

    return [
        {
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("content", ""),  # Tavily's clean page extract
        }
        for r in results
    ]
