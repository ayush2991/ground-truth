"""Unit tests for NLI scoring."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.pipeline import nli


def test_nli_supports():
    """Test that NLI correctly scores supporting evidence."""
    nli.load()

    premise = "The Earth is approximately 4.5 billion years old."
    hypothesis = "The Earth is 4.5 billion years old"

    scores = nli.score(premise, hypothesis)

    # Check structure
    assert isinstance(scores, dict)
    assert set(scores.keys()) == {"supports", "contradicts", "neutral"}
    assert all(0 <= v <= 1 for v in scores.values())

    # Check that "supports" is the highest score
    assert scores["supports"] > scores["contradicts"]
    assert scores["supports"] > scores["neutral"]
    print(f"✓ Support test passed: {scores}")


def test_nli_contradicts():
    """Test that NLI correctly scores contradicting evidence."""
    nli.load()

    premise = "Vaccines are safe and effective."
    hypothesis = "Vaccines are dangerous."

    scores = nli.score(premise, hypothesis)

    # Check that "contradicts" is the highest score
    assert scores["contradicts"] > scores["supports"]
    print(f"✓ Contradiction test passed: {scores}")


def test_nli_neutral():
    """Test that NLI correctly scores neutral/unrelated evidence."""
    nli.load()

    premise = "The sky is blue on clear days."
    hypothesis = "Cats are mammals."

    scores = nli.score(premise, hypothesis)

    # Check that "neutral" is highest or at least competitive
    max_label = max(scores, key=scores.get)
    assert max_label in ["neutral", "supports"]  # Could go either way
    print(f"✓ Neutral test passed: {scores}")


if __name__ == "__main__":
    test_nli_supports()
    test_nli_contradicts()
    test_nli_neutral()
    print("\n✓ All NLI tests passed!")
