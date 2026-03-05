from pydantic import BaseModel


class TradePlan(BaseModel):
    asset_in: str
    asset_out: str
    amount: float
    max_slippage: float
    reasoning: str
    confidence: float
