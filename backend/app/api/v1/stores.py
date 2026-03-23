from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.store import Store
from app.schemas.store import StoreOut, StoreCreate

router = APIRouter()


@router.get("/", response_model=list[StoreOut])
async def list_stores(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Store).order_by(Store.created_at.desc()))
    return result.scalars().all()


@router.get("/{store_id}", response_model=StoreOut)
async def get_store(store_id: str, db: AsyncSession = Depends(get_db)):
    store = await db.get(Store, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.post("/", response_model=StoreOut)
async def create_store(data: StoreCreate, db: AsyncSession = Depends(get_db)):
    store = Store(name=data.name, niche=data.niche)
    db.add(store)
    await db.commit()
    await db.refresh(store)
    return store


@router.post("/{store_id}/pause")
async def pause_store(store_id: str, db: AsyncSession = Depends(get_db)):
    store = await db.get(Store, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    store.status = "paused"
    await db.commit()
    return {"status": "paused"}


@router.post("/{store_id}/resume")
async def resume_store(store_id: str, db: AsyncSession = Depends(get_db)):
    store = await db.get(Store, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    store.status = "active"
    await db.commit()
    return {"status": "active"}
