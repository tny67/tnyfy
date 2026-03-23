from datetime import datetime

from pydantic import BaseModel


class StoreOut(BaseModel):
    id: str
    name: str
    shopify_domain: str | None
    status: str
    niche: str | None
    monthly_revenue: float
    created_at: datetime

    model_config = {"from_attributes": True}


class StoreCreate(BaseModel):
    name: str
    niche: str | None = None
