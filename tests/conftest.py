"""Pytest configuration and fixtures."""

import os
import sys

import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@pytest.fixture(autouse=True)
def reset_config_cache():
    """Reset config cache between tests to pick up env overrides."""
    from shared.config import get_config

    get_config.cache_clear()
    yield
    get_config.cache_clear()
