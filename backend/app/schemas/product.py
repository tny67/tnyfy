from datetime import datetime

from pydantic import BaseModel


class ProductOut(BaseModel):
    id: str
    store_id: str
    title: str
    description: str | None
    price: float
    cost_price: float
    supplier_url: str | None
    image_urls: list[str] | None
    status: str
    research_score: float
    conversion_rate: float
    created_at: datetime

    model_config = {"from_attributes": True}
