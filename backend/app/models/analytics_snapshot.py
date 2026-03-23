import uuid
from datetime import date, datetime

from sqlalchemy import String, Integer, Float, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AnalyticsSnapshot(Base):
    __tablename__ = "analytics_snapshots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    store_id: Mapped[str] = mapped_column(String(36), ForeignKey("stores.id"))
    date: Mapped[date] = mapped_column(Date)
    revenue: Mapped[float] = mapped_column(Float, default=0.0)
    orders_count: Mapped[int] = mapped_column(Integer, default=0)
    profit: Mapped[float] = mapped_column(Float, default=0.0)
    conversion_rate: Mapped[float] = mapped_column(Float, default=0.0)
    visitors: Mapped[int] = mapped_column(Integer, default=0)
    top_products: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    ad_spend: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
