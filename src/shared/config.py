"""Environment-based configuration."""

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@lru_cache
def get_config() -> dict:
    """Load configuration from environment variables."""
    return {
        "redis_host": os.getenv("REDIS_HOST", "localhost"),
        "redis_port": int(os.getenv("REDIS_PORT", "6379")),
        "redis_db": int(os.getenv("REDIS_DB", "0")),
        "channel_day_ahead": os.getenv("REDIS_CHANNEL_DAY_AHEAD", "prices:day-ahead"),
        "channel_real_time": os.getenv("REDIS_CHANNEL_REAL_TIME", "prices:real-time"),
        "api_host": os.getenv("API_HOST", "0.0.0.0"),
        "api_port": int(os.getenv("API_PORT", "8000")),
        "threshold_low_cents": float(os.getenv("THRESHOLD_LOW_CENTS", "20.0")),
        "threshold_high_cents": float(os.getenv("THRESHOLD_HIGH_CENTS", "80.0")),
    }
