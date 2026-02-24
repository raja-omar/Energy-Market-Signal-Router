"""Shared Redis connection client."""

import json
from typing import Any

import redis
from redis.connection import ConnectionPool

from .config import get_config
from .models import PriceSignal


def get_redis_pool() -> ConnectionPool:
    """Create a Redis connection pool."""
    config = get_config()
    return ConnectionPool(
        host=config["redis_host"],
        port=config["redis_port"],
        db=config["redis_db"],
        decode_responses=True,
    )


def get_redis_client() -> redis.Redis:
    """Get a Redis client using the shared pool."""
    return redis.Redis(connection_pool=get_redis_pool())


def serialize_signal(signal: PriceSignal) -> str:
    """Serialize PriceSignal to JSON string."""
    return signal.model_dump_json()


def deserialize_signal(data: str) -> PriceSignal:
    """Deserialize JSON string to PriceSignal."""
    return PriceSignal.model_validate_json(data)


def publish_signal(client: redis.Redis, channel: str, signal: PriceSignal) -> int:
    """Publish a price signal to a Redis channel. Returns number of subscribers notified."""
    return client.publish(channel, serialize_signal(signal))
