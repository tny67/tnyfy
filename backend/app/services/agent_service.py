"""
Agent service - Logging and cost tracking for AI agents.
"""

import logging
from datetime import date

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent_log import AgentLog
from app.config import settings

logger = logging.getLogger(__name__)


async def log_agent_run(
    db: AsyncSession,
    agent_type: str,
    action: str,
    status: str,
    store_id: str | None = None,
    input_data: dict | None = None,
    output_data: dict | None = None,
    tokens_used: int = 0,
    cost_usd: float = 0.0,
    duration_ms: int = 0,
) -> AgentLog:
    log = AgentLog(
        store_id=store_id,
        agent_type=agent_type,
        action=action,
        status=status,
        input_data=input_data,
        output_data=output_data,
        tokens_used=tokens_used,
        cost_usd=cost_usd,
        duration_ms=duration_ms,
    )
    db.add(log)
    await db.commit()
    return log


async def get_daily_cost(db: AsyncSession) -> float:
    result = await db.execute(
        select(func.sum(AgentLog.cost_usd)).where(
            func.date(AgentLog.created_at) == date.today()
        )
    )
    return result.scalar() or 0.0


async def check_budget(db: AsyncSession) -> bool:
    """Check if we're still within the daily budget."""
    daily_cost = await get_daily_cost(db)
    within_budget = daily_cost < settings.agent_daily_budget
    if not within_budget:
        logger.warning(
            f"Daily budget exceeded: ${daily_cost:.2f} / ${settings.agent_daily_budget:.2f}"
        )
    return within_budget
