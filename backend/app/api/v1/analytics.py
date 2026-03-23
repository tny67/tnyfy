from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.store import Store
from app.models.order import Order
from app.models.agent_log import AgentLog
from app.schemas.analytics import AnalyticsOverview

router = APIRouter()


@router.get("/overview", response_model=AnalyticsOverview)
async def overview(db: AsyncSession = Depends(get_db)):
    # Active stores count
    stores_result = await db.execute(
        select(func.count()).select_from(Store).where(Store.status == "active")
    )
    active_stores = stores_result.scalar() or 0

    # Total revenue & orders
    orders_result = await db.execute(
        select(func.sum(Order.total_price), func.count(), func.sum(Order.profit))
    )
    row = orders_result.one()
    total_revenue = row[0] or 0.0
    total_orders = row[1] or 0
    total_profit = row[2] or 0.0

    # AI cost today
    cost_result = await db.execute(
        select(func.sum(AgentLog.cost_usd)).where(
            func.date(AgentLog.created_at) == date.today()
        )
    )
    ai_cost_today = cost_result.scalar() or 0.0

    return AnalyticsOverview(
        total_revenue=total_revenue,
        total_orders=total_orders,
        total_profit=total_profit,
        active_stores=active_stores,
        ai_cost_today=ai_cost_today,
    )
