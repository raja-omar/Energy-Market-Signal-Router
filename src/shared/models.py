"""Pydantic models for price signals and trading decisions."""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class MarketType(str, Enum):
    """Electricity market type."""

    DAY_AHEAD = "day-ahead"
    REAL_TIME = "real-time"


class PriceSignal(BaseModel):
    """Electricity market price signal."""

    timestamp: datetime = Field(..., description="When the price was observed")
    market_type: MarketType = Field(..., description="DA or RT market")
    price_cents: float = Field(..., gt=0, description="Price in cents per kWh")
    region: str = Field(default="CAISO", description="Market region")


class TradingAction(str, Enum):
    """Battery trading action."""

    CHARGE = "charge"
    DISCHARGE = "discharge"
    HOLD = "hold"


class TradingDecision(BaseModel):
    """Output of the trading algorithm."""

    signal: PriceSignal
    action: TradingAction
    reason: str
