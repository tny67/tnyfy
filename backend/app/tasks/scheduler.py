"""
Task scheduler for Tnyfy's autonomous cycle.

Uses APScheduler to run the orchestrator on a schedule.
"""

import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.agents.orchestrator import orchestrator

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


def setup_scheduler():
    """Configure and start the task scheduler."""

    # Run orchestrator every hour
    scheduler.add_job(
        orchestrator.run_cycle,
        "interval",
        hours=1,
        id="orchestrator_cycle",
        name="Tnyfy Orchestrator Cycle",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("📅 Scheduler started - Orchestrator will run every hour")


def stop_scheduler():
    """Stop the scheduler gracefully."""
    scheduler.shutdown(wait=False)
    logger.info("📅 Scheduler stopped")
