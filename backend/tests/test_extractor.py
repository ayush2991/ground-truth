"""Unit tests for claim extraction."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.pipeline import extractor


def test_extractor_simple():
    """Test claim extraction on a simple paragraph."""
    extractor.load()

    text = (
        "The Earth orbits around the Sun. "
        "It takes approximately 365 days to complete one orbit. "
        "The Moon is Earth's only natural satellite."
    )

    claims = extractor.extract(text)

    # Check that we got some claims
    assert isinstance(claims, list)
    assert len(claims) > 0
    assert len(claims) <= 10

    # Check that all claims are non-empty strings
    assert all(isinstance(c, str) and len(c) > 0 for c in claims)

    print(f"✓ Extracted {len(claims)} claims:")
    for i, claim in enumerate(claims, 1):
        print(f"  {i}. {claim}")


def test_extractor_complex():
    """Test claim extraction on a longer paragraph."""
    extractor.load()

    text = (
        "Climate change is primarily driven by human activities. "
        "The burning of fossil fuels releases greenhouse gases into the atmosphere. "
        "These gases trap heat and cause global temperatures to rise. "
        "Rising temperatures lead to melting ice caps and rising sea levels. "
        "This threatens coastal communities and ecosystems worldwide."
    )

    claims = extractor.extract(text)

    # Check basic structure
    assert isinstance(claims, list)
    assert 1 <= len(claims) <= 10  # Should extract at least one claim

    # All claims should be non-empty
    assert all(isinstance(c, str) and len(c) > 0 for c in claims)

    print(f"\n✓ Extracted {len(claims)} claims from complex text:")
    for i, claim in enumerate(claims, 1):
        print(f"  {i}. {claim}")


def test_extractor_compound_sentences():
    """Regression test: compound sentences must produce multiple claims, not one."""
    extractor.load()

    text = (
        "Gemini 3 is the best LLM model, often outperforming GPT 5 by 20%. \n"
        " Gemini also outperforms almost every known anthropic model."
    )

    claims = extractor.extract(text)

    # Must split into at least 2 distinct claims (not merge into one string)
    assert len(claims) >= 2, f"Expected >= 2 claims, got {len(claims)}: {claims}"

    # No single claim should contain two separate factual assertions joined by a period
    for claim in claims:
        sentences = [s.strip() for s in claim.split(".") if s.strip()]
        assert len(sentences) <= 1, (
            f"Claim appears to contain multiple sentences: {claim!r}"
        )

    print(f"\n✓ Extracted {len(claims)} claims from compound sentence input:")
    for i, claim in enumerate(claims, 1):
        print(f"  {i}. {claim}")


if __name__ == "__main__":
    test_extractor_simple()
    test_extractor_complex()
    test_extractor_compound_sentences()
    print("\n✓ All extractor tests passed!")
