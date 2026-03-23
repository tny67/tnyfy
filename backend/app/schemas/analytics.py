from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    total_revenue: float = 0.0
    total_orders: int = 0
    total_profit: float = 0.0
    active_stores: int = 0
    conversion_rate: float = 0.0
    ai_cost_today: float = 0.0
