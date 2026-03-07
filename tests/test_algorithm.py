"""Unit tests for the trading algorithm."""

import os
from datetime import datetime, timezone

import pytest

from shared.models import MarketType, PriceSignal
from trading_consumer.algorithm import decide


def test_charge_when_below_threshold():
    """CHARGE when price is below threshold_low."""
    os.environ["THRESHOLD_LOW_CENTS"] = "30.0"
    os.environ["THRESHOLD_HIGH_CENTS"] = "70.0"
    signal = PriceSignal(
        timestamp=datetime.now(timezone.utc),
        market_type=MarketType.DAY_AHEAD,
        price_cents=15.0,
    )
    decision = decide(signal)
    assert decision.action.value == "charge"


def test_discharge_when_above_threshold():
    """DISCHARGE when price is above threshold_high."""
    os.environ["THRESHOLD_LOW_CENTS"] = "30.0"
    os.environ["THRESHOLD_HIGH_CENTS"] = "70.0"
    signal = PriceSignal(
        timestamp=datetime.now(timezone.utc),
        market_type=MarketType.REAL_TIME,
        price_cents=85.0,
    )
    decision = decide(signal)
    assert decision.action.value == "discharge"


def test_hold_when_in_range():
    """HOLD when price is between thresholds."""
    os.environ["THRESHOLD_LOW_CENTS"] = "30.0"
    os.environ["THRESHOLD_HIGH_CENTS"] = "70.0"
    signal = PriceSignal(
        timestamp=datetime.now(timezone.utc),
        market_type=MarketType.DAY_AHEAD,
        price_cents=50.0,
    )
    decision = decide(signal)
    assert decision.action.value == "hold"
