from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.product import Product
from app.schemas.product import ProductOut

router = APIRouter()


@router.get("/", response_model=list[ProductOut])
async def list_products(
    store_id: str | None = None, db: AsyncSession = Depends(get_db)
):
    query = select(Product).order_by(Product.research_score.desc())
    if store_id:
        query = query.where(Product.store_id == store_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: str, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
