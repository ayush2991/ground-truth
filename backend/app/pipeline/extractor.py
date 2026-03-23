"""Claim extraction module using T5-based model."""

import nltk
from transformers import pipeline as hf_pipeline

nltk.download("punkt_tab", quiet=True)
from nltk.tokenize import sent_tokenize  # noqa: E402

_pipe = None


def load():
    """Load the T5 claim extraction model at startup."""
    global _pipe
    print("Loading T5 claim extraction model...")
    _pipe = hf_pipeline(
        "text2text-generation",
        model="Babelscape/t5-base-summarization-claim-extractor",
        device=-1,  # CPU; change to 0 for GPU
    )
    print("T5 claim extraction model loaded.")


def extract(text: str) -> list[str]:
    """
    Extract discrete factual claims from text.

    Args:
        text: The input text to extract claims from

    Returns:
        A list of extracted claims (strings), capped at 10
    """
    if _pipe is None:
        raise RuntimeError("Extractor model not loaded. Call load() first.")

    # Run inference
    result = _pipe(text, max_new_tokens=512)
    generated_text = result[0]["generated_text"]

    # The model outputs claims separated by periods on a single line (not newlines).
    # Split on newlines first (in case future model versions use them), then apply
    # sentence tokenization to split any remaining period-delimited claims.
    claims = []
    for chunk in generated_text.split("\n"):
        chunk = chunk.strip()
        if chunk:
            claims.extend(sent_tokenize(chunk))

    claims = [c.strip() for c in claims if c.strip()]

    # Cap at 10 claims
    claims = claims[:10]

    return claims
