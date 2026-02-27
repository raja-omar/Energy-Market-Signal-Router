"""Publish price signals to Redis channels."""

from shared.models import MarketType, PriceSignal
from shared.redis_client import get_redis_client, publish_signal
from shared.config import get_config


def get_channel_for_market(market_type: MarketType) -> str:
    """Map market type to Redis channel name."""
    config = get_config()
    if market_type == MarketType.DAY_AHEAD:
        return config["channel_day_ahead"]
    return config["channel_real_time"]


def publish(signal: PriceSignal) -> int:
    """Publish a price signal to the appropriate Redis channel."""
    client = get_redis_client()
    channel = get_channel_for_market(signal.market_type)
    return publish_signal(client, channel, signal)
