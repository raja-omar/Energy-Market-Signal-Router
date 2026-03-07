"""Integration test: publish signals, consumer receives and processes."""

import os
import subprocess
import time
from datetime import datetime, timezone

import pytest
import redis

from shared.models import MarketType, PriceSignal
from shared.redis_client import deserialize_signal, get_redis_client, publish_signal


@pytest.fixture
def redis_client():
    """Skip if Redis is not available."""
    try:
        client = redis.Redis(host="localhost", port=6379, decode_responses=True)
        client.ping()
        return client
    except redis.ConnectionError:
        pytest.skip("Redis not running (start with: docker compose up -d redis)")


def test_redis_publish_subscribe_roundtrip(redis_client):
    """
    Publish a price signal to Redis, subscribe and verify it is received.
    """
    os.environ["REDIS_HOST"] = "localhost"
    os.environ["REDIS_PORT"] = "6379"

    received: list[PriceSignal] = []
    pubsub = redis_client.pubsub()
    pubsub.subscribe("prices:day-ahead")

    def listener():
        for msg in pubsub.listen():
            if msg["type"] == "message":
                received.append(deserialize_signal(msg["data"]))
                break

    import threading

    t = threading.Thread(target=listener)
    t.start()

    time.sleep(0.2)  # Allow subscriber to connect

    signal = PriceSignal(
        timestamp=datetime.now(timezone.utc),
        market_type=MarketType.DAY_AHEAD,
        price_cents=25.0,
    )
    publish_signal(redis_client, "prices:day-ahead", signal)

    t.join(timeout=2)

    assert len(received) == 1
    assert received[0].price_cents == 25.0
    assert received[0].market_type == MarketType.DAY_AHEAD
