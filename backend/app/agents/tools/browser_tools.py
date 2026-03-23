"""
Playwright browser automation tools for creating Shopify stores.

Uses headless Chromium to automate store creation via the Shopify Partner Dashboard.
"""

import logging
import asyncio

from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)


async def create_shopify_development_store(
    partner_email: str,
    partner_password: str,
    store_name: str,
) -> dict:
    """Create a development store via the Shopify Partner Dashboard."""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            )
            page = await context.new_page()

            # Step 1: Navigate to Shopify Partner login
            logger.info("Navigating to Shopify Partner login...")
            await page.goto("https://partners.shopify.com/organizations")
            await page.wait_for_load_state("networkidle")

            # Step 2: Login
            logger.info("Logging in to Shopify Partner...")
            email_input = page.locator('input[name="account[email]"], input[type="email"]')
            if await email_input.count() > 0:
                await email_input.fill(partner_email)
                submit_btn = page.locator('button[type="submit"]')
                await submit_btn.click()
                await page.wait_for_load_state("networkidle")

                # Password step
                password_input = page.locator('input[name="account[password]"], input[type="password"]')
                if await password_input.count() > 0:
                    await password_input.fill(partner_password)
                    await page.locator('button[type="submit"]').click()
                    await page.wait_for_load_state("networkidle")

            # Step 3: Navigate to store creation
            logger.info("Navigating to store creation...")
            await asyncio.sleep(2)

            # Find the "Stores" link and navigate
            stores_link = page.locator('a[href*="/stores"], a:has-text("Stores")')
            if await stores_link.count() > 0:
                await stores_link.first.click()
                await page.wait_for_load_state("networkidle")

            # Step 4: Click "Add store" or "Create store"
            add_store_btn = page.locator('a:has-text("Add store"), button:has-text("Add store"), a:has-text("Create store")')
            if await add_store_btn.count() > 0:
                await add_store_btn.first.click()
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(2)

            # Step 5: Select "Development store"
            dev_store_option = page.locator('text=Development store, label:has-text("Development")')
            if await dev_store_option.count() > 0:
                await dev_store_option.first.click()

            # Step 6: Fill store name
            store_name_input = page.locator('input[name*="store_name"], input[placeholder*="store name"]')
            if await store_name_input.count() > 0:
                await store_name_input.fill(store_name)

            # Step 7: Submit
            create_btn = page.locator('button:has-text("Create"), button[type="submit"]')
            if await create_btn.count() > 0:
                await create_btn.last.click()
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(5)

            # Get the resulting URL to determine the store domain
            current_url = page.url
            logger.info(f"Current URL after creation: {current_url}")

            await browser.close()

            # Extract store domain from URL
            store_domain = None
            if "myshopify.com" in current_url or ".shopify.com" in current_url:
                store_domain = f"{store_name.lower().replace(' ', '-')}.myshopify.com"

            return {
                "success": True,
                "store_name": store_name,
                "store_domain": store_domain or f"{store_name.lower().replace(' ', '-')}.myshopify.com",
                "url": current_url,
                "note": "Store creation attempted via Playwright automation",
            }

    except Exception as e:
        logger.error(f"Store creation failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "note": "Shopify may require 2FA or CAPTCHA - check Partner Dashboard manually",
        }
