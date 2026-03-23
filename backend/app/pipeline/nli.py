"""Natural Language Inference module using DeBERTa."""

from transformers import pipeline as hf_pipeline

_pipe = None


def load():
    """Load the DeBERTa NLI model at startup."""
    global _pipe
    print("Loading DeBERTa NLI model...")
    _pipe = hf_pipeline(
        "text-classification",
        model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli",
        device=-1,  # CPU; change to 0 for GPU
        top_k=None,  # Return all 3 labels with scores
    )
    print("DeBERTa NLI model loaded.")


def score(premise: str, hypothesis: str) -> dict[str, float]:
    """
    Score the relationship between a premise and hypothesis.

    Args:
        premise: The text to check against (max 1500 chars, ~512 tokens)
        hypothesis: The claim to verify

    Returns:
        A dict with keys "supports", "contradicts", "neutral" and float values (0-1)
    """
    if _pipe is None:
        raise RuntimeError("NLI model not loaded. Call load() first.")

    # Truncate premise to avoid token limit
    truncated = premise[:1500]

    # Run inference
    result = _pipe(truncated, text_pair=hypothesis)[0]  # Returns list of {label, score} dicts

    # Map DeBERTa labels to our verdict labels
    label_map = {
        "entailment": "supports",
        "contradiction": "contradicts",
        "neutral": "neutral",
    }

    # Convert to dict with our labels
    scores = {}
    for item in result:
        label = label_map.get(item["label"].lower(), item["label"].lower())
        scores[label] = item["score"]

    # Ensure all three keys exist
    for verdict in ["supports", "contradicts", "neutral"]:
        scores.setdefault(verdict, 0.0)

    return scores
