"""
Product service - Business logic for product management.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product


async def save_researched_product(
    db: AsyncSession,
    store_id: str,
    title: str,
    description: str = "",
    price: float = 0.0,
    cost_price: float = 0.0,
    supplier_url: str = "",
    image_urls: list[str] | None = None,
    research_score: float = 0.0,
    research_data: dict | None = None,
) -> Product:
    product = Product(
        store_id=store_id,
        title=title,
        description=description,
        price=price,
        cost_price=cost_price,
        supplier_url=supplier_url,
        image_urls=image_urls or [],
        research_score=research_score,
        research_data=research_data or {},
        status="researched",
    )
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def get_products_for_listing(db: AsyncSession, store_id: str, min_score: float = 70.0) -> list[Product]:
    """Get researched products with high scores ready for listing."""
    result = await db.execute(
        select(Product)
        .where(Product.store_id == store_id)
        .where(Product.status == "researched")
        .where(Product.research_score >= min_score)
        .order_by(Product.research_score.desc())
    )
    return list(result.scalars().all())


async def mark_product_listed(db: AsyncSession, product: Product, shopify_product_id: int) -> Product:
    product.shopify_product_id = shopify_product_id
    product.status = "live"
    await db.commit()
    return product
