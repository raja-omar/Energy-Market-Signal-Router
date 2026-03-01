"""Subscribe to Redis price channels and process signals."""

import logging
import signal as sig
import sys

from shared.config import get_config
from shared.redis_client import deserialize_signal, get_redis_client
from trading_consumer.algorithm import decide

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

_shutdown_requested = False


def _handle_sigterm(*args) -> None:
    global _shutdown_requested
    _shutdown_requested = True


def run() -> None:
    """Subscribe to price channels and process incoming signals."""
    global _shutdown_requested

    sig.signal(sig.SIGTERM, _handle_sigterm)
    sig.signal(sig.SIGINT, _handle_sigterm)

    config = get_config()
    client = get_redis_client()
    pubsub = client.pubsub()

    pubsub.subscribe(
        config["channel_day_ahead"],
        config["channel_real_time"],
    )

    logger.info(
        "Subscribed to %s, %s",
        config["channel_day_ahead"],
        config["channel_real_time"],
    )

    for message in pubsub.listen():
        if _shutdown_requested:
            logger.info("Shutdown requested, exiting")
            break

        if message["type"] != "message":
            continue

        try:
            signal = deserialize_signal(message["data"])
            decision = decide(signal)
            logger.info(
                "[%s] %s @ %.2f c/kWh -> %s",
                signal.market_type.value,
                signal.timestamp.isoformat(),
                signal.price_cents,
                decision.action.value,
            )
        except Exception as e:
            logger.exception("Failed to process message: %s", e)

    pubsub.unsubscribe()
    pubsub.close()
