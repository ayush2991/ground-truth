"""Sentence relevance ranker using keyword overlap (TF-IDF style, no extra model)."""

import re

_STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "to", "of", "in", "on",
    "at", "by", "for", "with", "as", "from", "that", "this", "it",
    "its", "and", "or", "but", "not", "no", "so", "if", "than", "then",
    "he", "she", "they", "we", "you", "i", "his", "her", "their", "our",
}


def _tokens(text: str) -> set[str]:
    words = re.findall(r"\b[a-z0-9]+\b", text.lower())
    return {w for w in words if w not in _STOPWORDS and len(w) > 2}


def top_sentences(text: str, claim: str, k: int = 3) -> str:
    """
    Return the k sentences from text most relevant to the claim, joined as a string.

    Args:
        text: Source text to extract sentences from
        claim: The claim being verified
        k: Number of top sentences to return

    Returns:
        Joined string of the most relevant sentences, or first 500 chars as fallback.
    """
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 15]
    if not sentences:
        return text[:500]

    claim_tokens = _tokens(claim)

    scored = [(len(claim_tokens & _tokens(sent)), sent) for sent in sentences]
    scored.sort(key=lambda x: x[0], reverse=True)

    top = [sent for score, sent in scored[:k] if score > 0]

    # Fallback to first k sentences if no overlap found
    return " ".join(top) if top else " ".join(sentences[:k])
