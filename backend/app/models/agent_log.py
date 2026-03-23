import uuid
from datetime import datetime

from sqlalchemy import String, Integer, Float, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AgentLog(Base):
    __tablename__ = "agent_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    store_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("stores.id"), nullable=True)
    agent_type: Mapped[str] = mapped_column(String(50))
    action: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(
        Enum("started", "running", "completed", "failed", name="agent_log_status"),
        default="started",
    )
    input_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    output_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    tokens_used: Mapped[int] = mapped_column(Integer, default=0)
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
