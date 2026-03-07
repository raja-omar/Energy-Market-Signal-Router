"""Unit tests for the price signal simulator."""

from datetime import datetime

import pytest

from signal_ingestion.simulator import generate_n_signals


def test_generate_n_signals_returns_correct_count():
    """generate_n_signals returns exactly n signals."""
    signals = generate_n_signals(10)
    assert len(signals) == 10


def test_generate_n_signals_has_valid_price_bounds():
    """Generated prices are positive and within reasonable bounds."""
    signals = generate_n_signals(100)
    for s in signals:
        assert s.price_cents >= 5.0
        assert s.price_cents < 200.0  # Sanity upper bound


def test_generate_n_signals_includes_both_market_types():
    """Generated signals include both day-ahead and real-time."""
    signals = generate_n_signals(20)
    types = {s.market_type.value for s in signals}
    assert "day-ahead" in types
    assert "real-time" in types


def test_generate_n_signals_respects_start_time():
    """Generated signals use provided start time."""
    start = datetime(2025, 6, 15, 12, 0, 0)
    signals = generate_n_signals(2, start=start)
    assert signals[0].timestamp == start
