"""
Shopify tools for agents - wraps the Shopify GraphQL client.
"""

import logging

from app.integrations.shopify.client import ShopifyClient

logger = logging.getLogger(__name__)


async def verify_store_connection(domain: str, access_token: str) -> dict:
    """Verify that Shopify API credentials work."""
    try:
        client = ShopifyClient(domain, access_token)
        data = await client.get_shop_info()
        shop = data.get("shop", {})
        return {
            "connected": True,
            "name": shop.get("name"),
            "email": shop.get("email"),
            "domain": shop.get("primaryDomain", {}).get("host"),
            "plan": shop.get("plan", {}).get("displayName"),
            "currency": shop.get("currencyCode"),
        }
    except Exception as e:
        return {"connected": False, "error": str(e)}


async def create_shopify_product(
    domain: str,
    access_token: str,
    title: str,
    description_html: str,
    price: float,
    images: list[str] | None = None,
) -> dict:
    """Create a product on a Shopify store."""
    try:
        client = ShopifyClient(domain, access_token)
        result = await client.create_product(title, description_html, price, images)

        product_data = result.get("productCreate", {})
        errors = product_data.get("userErrors", [])
        if errors:
            return {"created": False, "errors": errors}

        product = product_data.get("product", {})
        return {
            "created": True,
            "shopify_product_id": product.get("id"),
            "title": product.get("title"),
            "handle": product.get("handle"),
        }
    except Exception as e:
        return {"created": False, "error": str(e)}


async def get_store_orders(domain: str, access_token: str, limit: int = 20) -> dict:
    """Get recent orders from a Shopify store."""
    try:
        client = ShopifyClient(domain, access_token)
        result = await client.get_orders(limit=limit)
        orders = result.get("orders", {}).get("edges", [])
        return {
            "success": True,
            "count": len(orders),
            "orders": [edge["node"] for edge in orders],
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
