"""Unit tests for the sentence relevance ranker."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.pipeline import ranker


def test_top_sentences_returns_relevant():
    """Most relevant sentences to the claim should be selected."""
    text = (
        "The Sun is a star at the center of the solar system. "
        "It is approximately 93 million miles from Earth. "
        "The Earth orbits the Sun once every 365 days. "
        "Jupiter is the largest planet in the solar system. "
        "Saturn has beautiful rings made of ice and rock."
    )
    claim = "The Earth orbits the Sun every 365 days."
    result = ranker.top_sentences(text, claim, k=2)

    assert "Earth" in result
    assert "365" in result or "orbits" in result
    print(f"✓ Relevant sentences selected: {result!r}")


def test_top_sentences_fallback_on_no_overlap():
    """Falls back to first k sentences when no keyword overlap."""
    text = "Alpha beta gamma. Delta epsilon zeta. Eta theta iota kappa."
    claim = "Something completely unrelated to the text."
    result = ranker.top_sentences(text, claim, k=2)

    # Should return some content (fallback)
    assert len(result) > 0
    print(f"✓ Fallback on no overlap: {result!r}")


def test_top_sentences_empty_text():
    """Returns empty-ish string for very short text."""
    result = ranker.top_sentences("Hi.", "Some claim.", k=3)
    assert isinstance(result, str)
    print(f"✓ Short text handled: {result!r}")


def test_top_sentences_respects_k():
    """Returns at most k sentences."""
    text = " ".join(f"Sentence number {i} about dogs." for i in range(20))
    claim = "dogs"
    result = ranker.top_sentences(text, claim, k=2)

    # Result must be a subset of sentences from the original text — not all 20
    assert len(result) < len(text), "Should not return the entire text"
    # With k=2, we expect only 2 of the 20 sentences to be selected
    selected = [s for s in result.split(". ") if s.strip()]
    assert len(selected) <= 2
    print(f"✓ Respects k=2, got {len(selected)} sentences")


if __name__ == "__main__":
    test_top_sentences_returns_relevant()
    test_top_sentences_fallback_on_no_overlap()
    test_top_sentences_empty_text()
    test_top_sentences_respects_k()
    print("\n✓ All ranker tests passed!")
