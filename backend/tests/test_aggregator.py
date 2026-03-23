"""Unit tests for verdict aggregation."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.pipeline import aggregator


def test_aggregate_supports():
    """Test aggregation when all sources support."""
    nli_results = [
        {"supports": 0.9, "contradicts": 0.05, "neutral": 0.05},
        {"supports": 0.85, "contradicts": 0.1, "neutral": 0.05},
        {"supports": 0.92, "contradicts": 0.04, "neutral": 0.04},
    ]

    result = aggregator.aggregate(nli_results)

    assert result["verdict"] == "supports"
    assert result["confidence"] > 0.8
    print(f"✓ Supports aggregation: verdict={result['verdict']}, confidence={result['confidence']}")


def test_aggregate_contradicts():
    """Test aggregation when sources contradict."""
    nli_results = [
        {"supports": 0.05, "contradicts": 0.9, "neutral": 0.05},
        {"supports": 0.1, "contradicts": 0.85, "neutral": 0.05},
        {"supports": 0.08, "contradicts": 0.88, "neutral": 0.04},
    ]

    result = aggregator.aggregate(nli_results)

    assert result["verdict"] == "contradicts"
    assert result["confidence"] > 0.8
    print(f"✓ Contradicts aggregation: verdict={result['verdict']}, confidence={result['confidence']}")


def test_aggregate_mixed():
    """Test aggregation with mixed verdicts."""
    nli_results = [
        {"supports": 0.7, "contradicts": 0.15, "neutral": 0.15},
        {"supports": 0.6, "contradicts": 0.2, "neutral": 0.2},
        {"supports": 0.5, "contradicts": 0.3, "neutral": 0.2},
    ]

    result = aggregator.aggregate(nli_results)

    assert result["verdict"] == "supports"  # Supports still wins with mixed results
    assert 0 <= result["confidence"] <= 1
    print(f"✓ Mixed aggregation: verdict={result['verdict']}, confidence={result['confidence']}")


def test_aggregate_empty():
    """Test aggregation with no results."""
    nli_results = []

    result = aggregator.aggregate(nli_results)

    assert result["verdict"] == "neutral"
    assert result["confidence"] == 0.0
    print(f"✓ Empty aggregation: verdict={result['verdict']}, confidence={result['confidence']}")


if __name__ == "__main__":
    test_aggregate_supports()
    test_aggregate_contradicts()
    test_aggregate_mixed()
    test_aggregate_empty()
    print("\n✓ All aggregator tests passed!")
