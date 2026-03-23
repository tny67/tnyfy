"""
Orchestrator - The brain that coordinates all agents.

This is NOT an AI agent - it's a Python scheduler that decides
which agents to run and when, based on system state.
"""

import logging
from datetime import datetime, timedelta

from app.database import async_session
from app.models.store import Store
from app.models.product import Product
from app.agents.niche_finder import NicheFinderAgent
from app.agents.product_research import ProductResearchAgent
from app.agents.store_creator import StoreCreatorAgent
from app.agents.listing_agent import ListingAgent
from app.services.agent_service import log_agent_run, check_budget
from app.services.store_service import get_active_stores, get_stores_by_status
from app.services.product_service import get_products_for_listing
from app.config import settings

logger = logging.getLogger(__name__)


class Orchestrator:
    """Coordinates all Tnyfy agents. Runs on a schedule."""

    def __init__(self):
        self.is_running = False
        self.last_niche_search: datetime | None = None

    async def run_cycle(self):
        """Run one orchestration cycle. Called every hour by the scheduler."""
        if self.is_running:
            logger.info("Orchestrator already running, skipping cycle")
            return

        self.is_running = True
        logger.info("--- Orchestrator cycle started ---")

        try:
            async with async_session() as db:
                # Check budget first
                if not await check_budget(db):
                    logger.warning("Daily budget exceeded - skipping cycle")
                    await log_agent_run(
                        db, "orchestrator", "budget_check", "failed",
                        output_data={"reason": "daily_budget_exceeded"},
                    )
                    return

                # 1. Check if we need new niches (weekly)
                await self._maybe_find_niches(db)

                # 2. Check stores that need creation/setup
                await self._process_creating_stores(db)

                # 3. Research products for active stores
                await self._research_products_for_stores(db)

                # 4. List high-scoring products
                await self._list_approved_products(db)

                await log_agent_run(
                    db, "orchestrator", "cycle_complete", "completed",
                )
                logger.info("--- Orchestrator cycle completed ---")

        except Exception as e:
            logger.error(f"Orchestrator error: {e}")
            try:
                async with async_session() as db:
                    await log_agent_run(
                        db, "orchestrator", "cycle_error", "failed",
                        output_data={"error": str(e)},
                    )
            except Exception:
                pass
        finally:
            self.is_running = False

    async def _maybe_find_niches(self, db):
        """Find new niches if we haven't done it this week."""
        should_search = (
            self.last_niche_search is None
            or datetime.utcnow() - self.last_niche_search > timedelta(days=7)
        )
        if not should_search:
            return

        logger.info("Running niche discovery...")
        agent = NicheFinderAgent()
        result = agent.run("Trouve 3 niches e-commerce rentables en France pour 2026. Analyse les tendances actuelles.")

        await log_agent_run(
            db, agent.agent_type, "niche_discovery", "completed" if result.success else "failed",
            output_data={"output": result.output, "niches_found": len(agent.found_niches)},
            tokens_used=agent.total_tokens,
            cost_usd=agent.total_cost,
            duration_ms=result.duration_ms,
        )

        # Create stores for top niches
        if result.success and agent.found_niches:
            for niche in agent.found_niches[:2]:  # Max 2 new stores per cycle
                if niche.get("score", 0) >= 70:
                    store = Store(
                        name=niche["name"],
                        niche=niche["name"],
                        status="creating",
                    )
                    db.add(store)
                    logger.info(f"Created store for niche: {niche['name']}")
            await db.commit()

        self.last_niche_search = datetime.utcnow()

    async def _process_creating_stores(self, db):
        """Create Shopify stores that are in 'creating' status."""
        stores = await get_stores_by_status(db, "creating")
        if not stores:
            return

        for store in stores:
            if not settings.shopify_partner_email:
                logger.warning("No Shopify Partner credentials - cannot create stores")
                break

            logger.info(f"Creating Shopify store for: {store.name}")
            agent = StoreCreatorAgent()
            result = agent.run(
                f"Cree une boutique Shopify pour la niche '{store.niche}'. "
                f"Genere un nom de marque attractif."
            )

            await log_agent_run(
                db, agent.agent_type, f"create_store:{store.name}",
                "completed" if result.success else "failed",
                store_id=store.id,
                output_data={"output": result.output},
                tokens_used=agent.total_tokens,
                cost_usd=agent.total_cost,
                duration_ms=result.duration_ms,
            )

            if result.success:
                store.status = "setup"
                await db.commit()

    async def _research_products_for_stores(self, db):
        """Run product research for all active stores."""
        stores = await get_active_stores(db)
        if not stores:
            # Also research for stores in setup status
            stores = await get_stores_by_status(db, "setup")

        for store in stores[:3]:  # Max 3 stores per cycle
            logger.info(f"Researching products for store: {store.name} ({store.niche})")
            agent = ProductResearchAgent(store_id=store.id)
            result = agent.run(
                f"Recherche 5 produits gagnants pour la niche '{store.niche}'. "
                f"Trouve des produits avec un bon potentiel de marge et de vente."
            )

            await log_agent_run(
                db, agent.agent_type, f"research:{store.niche}",
                "completed" if result.success else "failed",
                store_id=store.id,
                output_data={
                    "output": result.output,
                    "products_found": len(agent.found_products),
                },
                tokens_used=agent.total_tokens,
                cost_usd=agent.total_cost,
                duration_ms=result.duration_ms,
            )

            # Save found products to DB
            for p in agent.found_products:
                product = Product(
                    store_id=store.id,
                    title=p["title"],
                    description=p.get("description", ""),
                    price=p.get("price", 0),
                    cost_price=p.get("cost_price", 0),
                    supplier_url=p.get("supplier_url", ""),
                    research_score=p.get("research_score", 0),
                    research_data=p.get("research_data"),
                    status="researched",
                )
                db.add(product)
            await db.commit()

    async def _list_approved_products(self, db):
        """List high-scoring products on Shopify stores."""
        stores = await get_active_stores(db)
        for store in stores:
            products = await get_products_for_listing(db, store.id)
            if not products:
                continue

            logger.info(f"Listing {len(products)} products on {store.name}")
            agent = ListingAgent()
            for product in products[:5]:  # Max 5 listings per store per cycle
                result = agent.run(
                    f"Cree une fiche produit optimisee pour '{product.title}'. "
                    f"Prix cout: {product.cost_price}EUR. Niche: {store.niche}. "
                    f"Publie-le sur la boutique."
                )
                await log_agent_run(
                    db, agent.agent_type, f"list:{product.title[:50]}",
                    "completed" if result.success else "failed",
                    store_id=store.id,
                    tokens_used=agent.total_tokens,
                    cost_usd=agent.total_cost,
                    duration_ms=result.duration_ms,
                )


# Singleton
orchestrator = Orchestrator()
