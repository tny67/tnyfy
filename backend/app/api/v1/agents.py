from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.agent_log import AgentLog
from app.schemas.agent import AgentStatusOut, AgentLogOut

router = APIRouter()

AGENT_TYPES = [
    "orchestrator",
    "niche_finder",
    "store_creator",
    "store_setup",
    "product_research",
    "listing_agent",
    "order_manager",
    "customer_service",
]


@router.get("/status", response_model=list[AgentStatusOut])
async def agent_statuses(db: AsyncSession = Depends(get_db)):
    statuses = []
    for agent_type in AGENT_TYPES:
        # Last run
        last_result = await db.execute(
            select(AgentLog)
            .where(AgentLog.agent_type == agent_type)
            .order_by(AgentLog.created_at.desc())
            .limit(1)
        )
        last_log = last_result.scalar_one_or_none()

        # Totals
        totals_result = await db.execute(
            select(func.count(), func.sum(AgentLog.cost_usd)).where(
                AgentLog.agent_type == agent_type
            )
        )
        row = totals_result.one()

        statuses.append(
            AgentStatusOut(
                agent_type=agent_type,
                status=last_log.status if last_log else "idle",
                last_run=last_log.created_at if last_log else None,
                total_runs=row[0] or 0,
                total_cost=row[1] or 0.0,
            )
        )
    return statuses


@router.get("/logs", response_model=list[AgentLogOut])
async def agent_logs(limit: int = 50, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AgentLog).order_by(AgentLog.created_at.desc()).limit(limit)
    )
    return result.scalars().all()
