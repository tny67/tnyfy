"""
Store service - Business logic for store management.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store import Store
from app.services.crypto_service import encrypt, decrypt


async def get_active_stores(db: AsyncSession) -> list[Store]:
    result = await db.execute(
        select(Store).where(Store.status == "active")
    )
    return list(result.scalars().all())


async def get_stores_by_status(db: AsyncSession, status: str) -> list[Store]:
    result = await db.execute(
        select(Store).where(Store.status == status)
    )
    return list(result.scalars().all())


async def create_store(db: AsyncSession, name: str, niche: str | None = None) -> Store:
    store = Store(name=name, niche=niche, status="creating")
    db.add(store)
    await db.commit()
    await db.refresh(store)
    return store


async def update_store_credentials(
    db: AsyncSession, store: Store, domain: str, access_token: str
) -> Store:
    store.shopify_domain = domain
    store.shopify_access_token = encrypt(access_token)
    store.status = "setup"
    await db.commit()
    await db.refresh(store)
    return store


async def activate_store(db: AsyncSession, store: Store) -> Store:
    store.status = "active"
    await db.commit()
    return store


def get_decrypted_token(store: Store) -> str:
    if store.shopify_access_token:
        return decrypt(store.shopify_access_token)
    return ""
