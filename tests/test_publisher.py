"""Unit tests for the publisher (requires Redis)."""

import os
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from shared.models import MarketType, PriceSignal


def test_get_channel_for_market():
    """Channel mapping is correct for each market type."""
    from signal_ingestion.publisher import get_channel_for_market

    os.environ["REDIS_CHANNEL_DAY_AHEAD"] = "prices:day-ahead"
    os.environ["REDIS_CHANNEL_REAL_TIME"] = "prices:real-time"
    assert get_channel_for_market(MarketType.DAY_AHEAD) == "prices:day-ahead"
    assert get_channel_for_market(MarketType.REAL_TIME) == "prices:real-time"


@patch("signal_ingestion.publisher.get_redis_client")
def test_publish_serializes_and_sends(get_redis_mock):
    """Publisher serializes signal and publishes to Redis."""
    from signal_ingestion.publisher import publish

    mock_client = MagicMock()
    mock_client.publish.return_value = 1
    get_redis_mock.return_value = mock_client

    signal = PriceSignal(
        timestamp=datetime.now(timezone.utc),
        market_type=MarketType.DAY_AHEAD,
        price_cents=42.5,
    )

    result = publish(signal)

    mock_client.publish.assert_called_once()
    call_args = mock_client.publish.call_args
    assert call_args[0][0] == "prices:day-ahead"
    assert "42.5" in call_args[0][1]
    assert result == 1
