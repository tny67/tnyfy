import uuid
from datetime import datetime

from sqlalchemy import String, Text, Enum, Float, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Store(Base):
    __tablename__ = "stores"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255))
    shopify_domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    shopify_access_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("creating", "setup", "active", "paused", "error", name="store_status"),
        default="creating",
    )
    niche: Mapped[str | None] = mapped_column(String(255), nullable=True)
    config_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    monthly_revenue: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
