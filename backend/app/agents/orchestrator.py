"""
Orchestrator - The brain that coordinates all agents.

This is NOT an AI agent - it's a Python scheduler that decides
which agents to run and when, based on system state.
"""

import asyncio
import logging
from datetime import datetime

from app.agents.niche_finder import NicheFinderAgent
from app.agents.product_research import ProductResearchAgent
from app.agents.store_creator import StoreCreatorAgent
from app.agents.store_setup import StoreSetupAgent
from app.agents.listing_agent import ListingAgent
from app.agents.order_manager import OrderManagerAgent
from app.agents.customer_service import CustomerServiceAgent

logger = logging.getLogger(__name__)


class Orchestrator:
    """Coordinates all Tnyfy agents. Runs on a schedule."""

    def __init__(self):
        self.is_running = False
        self.last_niche_search: datetime | None = None

    async def run_cycle(self):
        """Run one orchestration cycle. Called every hour."""
        if self.is_running:
            logger.info("Orchestrator already running, skipping cycle")
            return

        self.is_running = True
        logger.info("🔄 Orchestrator cycle started")

        try:
            # 1. Check if we need new niches (weekly)
            await self._maybe_find_niches()

            # 2. Check stores that need setup
            await self._process_pending_stores()

            # 3. Research products for active stores
            await self._research_products()

            # 4. Process product listings
            await self._process_listings()

            # 5. Handle pending orders
            await self._handle_orders()

            # 6. Handle customer service
            await self._handle_customer_service()

            logger.info("✅ Orchestrator cycle completed")

        except Exception as e:
            logger.error(f"❌ Orchestrator error: {e}")
        finally:
            self.is_running = False

    async def _maybe_find_niches(self):
        """Find new niches if we haven't recently."""
        # TODO: Check last niche search from DB
        # For now, placeholder
        logger.info("📊 Checking if niche research is needed...")

    async def _process_pending_stores(self):
        """Create and setup stores that are in 'creating' or 'setup' status."""
        # TODO: Query stores with pending status from DB
        logger.info("🏪 Checking for pending store setups...")

    async def _research_products(self):
        """Run product research for active stores."""
        # TODO: Query active stores and run ProductResearchAgent
        logger.info("🔍 Running product research...")

    async def _process_listings(self):
        """Publish approved products to Shopify."""
        # TODO: Query products with status 'researched' and score > 70
        logger.info("📝 Processing product listings...")

    async def _handle_orders(self):
        """Process pending orders."""
        # TODO: Query pending orders
        logger.info("📦 Handling pending orders...")

    async def _handle_customer_service(self):
        """Process open customer conversations."""
        # TODO: Query open conversations
        logger.info("💬 Handling customer service...")


# Singleton
orchestrator = Orchestrator()
