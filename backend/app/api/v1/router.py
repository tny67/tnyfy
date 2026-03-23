from fastapi import APIRouter

from app.api.v1 import stores, products, analytics, agents

api_router = APIRouter()

api_router.include_router(stores.router, prefix="/stores", tags=["stores"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
