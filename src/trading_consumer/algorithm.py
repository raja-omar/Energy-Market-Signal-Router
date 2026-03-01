"""Simple battery arbitrage trading algorithm: charge when low, discharge when high."""

from shared.config import get_config
from shared.models import PriceSignal, TradingAction, TradingDecision


def decide(signal: PriceSignal) -> TradingDecision:
    """
    Decide trading action based on price thresholds.

    - price < threshold_low: CHARGE (buy cheap)
    - price > threshold_high: DISCHARGE (sell high)
    - else: HOLD
    """
    config = get_config()
    low = config["threshold_low_cents"]
    high = config["threshold_high_cents"]

    if signal.price_cents < low:
        return TradingDecision(
            signal=signal,
            action=TradingAction.CHARGE,
            reason=f"Price {signal.price_cents} below threshold {low}",
        )
    if signal.price_cents > high:
        return TradingDecision(
            signal=signal,
            action=TradingAction.DISCHARGE,
            reason=f"Price {signal.price_cents} above threshold {high}",
        )
    return TradingDecision(
        signal=signal,
        action=TradingAction.HOLD,
        reason=f"Price {signal.price_cents} in range [{low}, {high}]",
    )
