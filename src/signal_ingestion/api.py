"""FastAPI application for price signal ingestion."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from shared.models import MarketType, PriceSignal
from signal_ingestion.publisher import publish
from signal_ingestion.simulator import generate_n_signals


app = FastAPI(
    title="Energy Market Price Signal API",
    description="Ingest and route electricity market price signals to trading algorithms.",
)


class PriceSignalInput(BaseModel):
    """Input schema for POST /prices."""

    timestamp: str
    market_type: str
    price_cents: float
    region: str = "CAISO"


@app.get("/health")
def health() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/prices")
def post_prices(payload: PriceSignalInput) -> dict:
    """
    Accept external price signals, validate, and publish to Redis.
    """
    from datetime import datetime

    try:
        market_type = MarketType(payload.market_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"market_type must be 'day-ahead' or 'real-time', got '{payload.market_type}'",
        )

    try:
        timestamp = datetime.fromisoformat(payload.timestamp.replace("Z", "+00:00"))
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="timestamp must be ISO 8601 format",
        )

    if payload.price_cents <= 0:
        raise HTTPException(status_code=400, detail="price_cents must be positive")

    signal = PriceSignal(
        timestamp=timestamp,
        market_type=market_type,
        price_cents=payload.price_cents,
        region=payload.region,
    )

    subscribers = publish(signal)
    return {
        "status": "published",
        "subscribers_notified": subscribers,
        "channel": f"prices:{payload.market_type}",
    }


@app.post("/simulate")
def simulate_signals(count: int = 5) -> dict:
    """
    Generate and publish simulated price signals. Useful for demos.
    """
    if count < 1 or count > 100:
        raise HTTPException(status_code=400, detail="count must be between 1 and 100")

    signals = generate_n_signals(count)
    total_subscribers = 0
    for s in signals:
        total_subscribers += publish(s)

    return {
        "status": "published",
        "signals_generated": count,
        "subscribers_notified": total_subscribers,
    }
