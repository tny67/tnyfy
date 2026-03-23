"""
Shopify Webhook handlers - receives real-time events from Shopify stores.
"""

import logging

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.order import Order
from app.websocket_manager import ws_manager

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/shopify/orders/create")
async def shopify_order_created(request: Request, db: AsyncSession = Depends(get_db)):
    """Handle new order webhook from Shopify."""
    body = await request.json()
    logger.info(f"New Shopify order received: {body.get('name', 'unknown')}")

    # TODO: Map to store_id from webhook headers (X-Shopify-Shop-Domain)
    order = Order(
        shopify_order_id=body.get("id"),
        customer_email=body.get("email", ""),
        total_price=float(body.get("total_price", 0)),
        status="new",
        order_data=body,
    )
    db.add(order)
    await db.commit()

    # Broadcast to dashboard
    await ws_manager.send_new_order({
        "order_name": body.get("name"),
        "email": body.get("email"),
        "total": body.get("total_price"),
    })

    return {"status": "received"}


@router.post("/shopify/orders/updated")
async def shopify_order_updated(request: Request):
    """Handle order update webhook from Shopify."""
    body = await request.json()
    logger.info(f"Shopify order updated: {body.get('name', 'unknown')}")
    # TODO: Update order status in DB
    return {"status": "received"}
