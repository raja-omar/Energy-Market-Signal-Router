"""Market price signal simulator with realistic intraday patterns."""

import math
import random
from datetime import datetime, timedelta, timezone
from typing import Iterator

from shared.models import MarketType, PriceSignal


def _day_ahead_price(hour: int, minute: int, base: float = 50.0) -> float:
    """Generate day-ahead price: higher during peak hours (8-18), lower overnight."""
    # Two peaks: morning (~9) and afternoon (~16)
    peak1 = math.exp(-((hour - 9) ** 2) / 8) * 40
    peak2 = math.exp(-((hour - 16) ** 2) / 8) * 50
    base_level = base + peak1 + peak2
    noise = random.gauss(0, 5)
    return max(5.0, base_level + noise)


def _real_time_price(da_price: float, volatility: float = 0.15) -> float:
    """Generate real-time price as DA price + volatility."""
    return max(5.0, da_price + random.gauss(0, da_price * volatility))


def generate_signals(
    start: datetime | None = None,
    interval_minutes: int = 60,
    region: str = "CAISO",
) -> Iterator[PriceSignal]:
    """
    Generate a stream of price signals with realistic intraday patterns.

    Yields PriceSignal objects for both day-ahead and real-time markets.
    """
    start = start or datetime.now(timezone.utc)
    current = start

    while True:
        hour = current.hour
        minute = current.minute

        da_price = _day_ahead_price(hour, minute)
        rt_price = _real_time_price(da_price)

        yield PriceSignal(
            timestamp=current,
            market_type=MarketType.DAY_AHEAD,
            price_cents=round(da_price, 2),
            region=region,
        )
        yield PriceSignal(
            timestamp=current,
            market_type=MarketType.REAL_TIME,
            price_cents=round(rt_price, 2),
            region=region,
        )

        current += timedelta(minutes=interval_minutes)


def generate_n_signals(
    n: int,
    start: datetime | None = None,
    interval_minutes: int = 60,
    region: str = "CAISO",
) -> list[PriceSignal]:
    """Generate exactly n price signals."""
    signals: list[PriceSignal] = []
    for signal in generate_signals(start, interval_minutes, region):
        signals.append(signal)
        if len(signals) >= n:
            break
    return signals
