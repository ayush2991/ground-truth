"""Verdict aggregation using weighted probability voting."""


def aggregate(nli_results: list[dict]) -> dict:
    """
    Aggregate NLI scores from multiple sources using weighted probability voting.

    Args:
        nli_results: A list of dicts with keys "supports", "contradicts", "neutral" (float 0-1)

    Returns:
        A dict with:
            - "verdict": one of "supports", "contradicts", "neutral"
            - "confidence": float 0-1
    """
    if not nli_results:
        return {
            "verdict": "neutral",
            "confidence": 0.0,
        }

    # Sum probabilities across all sources
    totals = {"supports": 0.0, "contradicts": 0.0, "neutral": 0.0}
    for result in nli_results:
        for verdict_type in ["supports", "contradicts", "neutral"]:
            totals[verdict_type] += result.get(verdict_type, 0.0)

    # Find winner
    winner = max(totals, key=totals.get)

    # Compute confidence as normalized score
    total_sum = sum(totals.values())
    confidence = totals[winner] / total_sum if total_sum > 0 else 0.0

    return {
        "verdict": winner,
        "confidence": round(confidence, 3),
    }
