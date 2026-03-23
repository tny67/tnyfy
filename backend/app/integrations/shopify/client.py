"""
Shopify GraphQL API Client.

Handles all communication with Shopify stores via their GraphQL Admin API.
"""

import httpx


class ShopifyClient:
    """Async Shopify GraphQL API client."""

    API_VERSION = "2025-01"

    def __init__(self, shop_domain: str, access_token: str):
        self.shop_domain = shop_domain
        self.access_token = access_token
        self.base_url = f"https://{shop_domain}/admin/api/{self.API_VERSION}/graphql.json"

    async def execute(self, query: str, variables: dict | None = None) -> dict:
        """Execute a GraphQL query against the Shopify Admin API."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                json={"query": query, "variables": variables or {}},
                headers={
                    "X-Shopify-Access-Token": self.access_token,
                    "Content-Type": "application/json",
                },
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()

            if "errors" in data:
                raise ShopifyAPIError(data["errors"])

            return data.get("data", {})

    async def get_shop_info(self) -> dict:
        """Get basic shop information."""
        query = """
        {
            shop {
                name
                email
                primaryDomain { url host }
                plan { displayName }
                currencyCode
            }
        }
        """
        return await self.execute(query)

    async def create_product(
        self,
        title: str,
        description_html: str,
        price: float,
        images: list[str] | None = None,
    ) -> dict:
        """Create a new product in the Shopify store."""
        query = """
        mutation productCreate($input: ProductInput!) {
            productCreate(input: $input) {
                product {
                    id
                    title
                    handle
                    status
                }
                userErrors {
                    field
                    message
                }
            }
        }
        """
        variables = {
            "input": {
                "title": title,
                "descriptionHtml": description_html,
                "variants": [{"price": str(price)}],
            }
        }
        if images:
            variables["input"]["images"] = [{"src": url} for url in images]

        return await self.execute(query, variables)

    async def get_orders(self, status: str = "any", limit: int = 50) -> dict:
        """Get orders from the store."""
        query = """
        query($first: Int!, $query: String) {
            orders(first: $first, query: $query, sortKey: CREATED_AT, reverse: true) {
                edges {
                    node {
                        id
                        name
                        email
                        totalPriceSet { shopMoney { amount currencyCode } }
                        displayFinancialStatus
                        displayFulfillmentStatus
                        createdAt
                    }
                }
            }
        }
        """
        variables = {"first": limit}
        if status != "any":
            variables["query"] = f"financial_status:{status}"
        return await self.execute(query, variables)


class ShopifyAPIError(Exception):
    """Raised when Shopify API returns errors."""

    def __init__(self, errors: list):
        self.errors = errors
        super().__init__(str(errors))
