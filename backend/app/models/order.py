import uuid
from datetime import datetime

from sqlalchemy import String, Float, BigInteger, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    store_id: Mapped[str] = mapped_column(String(36), ForeignKey("stores.id"))
    shopify_order_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    customer_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("customers.id"), nullable=True)
    customer_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    total_price: Mapped[float] = mapped_column(Float, default=0.0)
    profit: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(
        Enum("new", "processing", "fulfilled", "cancelled", "refunded", name="order_status"),
        default="new",
    )
    fulfillment_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    order_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
