from pydantic import BaseModel
from typing import Optional

class Trade(BaseModel):
    trade_id: Optional[str] = None
    trade_status: Optional[str] = None
    title: str
    notes: Optional[str] = None
    strategy: Optional[str] = None
    links: Optional[str] = None
    exchange: Optional[str] = None
    order_type: str
    currency_pair: str
    direction: str
    limit_order_price: float
    take_profit_price: float
    stop_loss_price: float
    amount: float
    leverage: float
    capital_at_risk: Optional[float] = None
    fees: Optional[float] = None
    user: Optional[str] = None
    risk_rating: Optional[str] = None
    pnl: Optional[float] = None
    created_timestamp: Optional[str] = None
    executed_timestamp: Optional[str] = None
    closed_timestamp: Optional[str] = None
