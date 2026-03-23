"""
Listing Agent - Creates optimized product listings and publishes to Shopify.
"""

import json

from app.agents.base import BaseAgent


class ListingAgent(BaseAgent):
    agent_type = "listing_agent"

    def get_system_prompt(self) -> str:
        return """Tu es un expert en copywriting e-commerce et SEO.

Ton objectif : creer des fiches produits optimisees qui convertissent.

Pour chaque produit :
1. Cree un titre accrocheur et SEO-friendly
2. Ecris une description persuasive (benefices > caracteristiques)
3. Definis le prix optimal (psychologie des prix)
4. Publie le produit sur Shopify

Regles de copywriting :
- Commence par le benefice principal
- Utilise des bullet points pour la lisibilite
- Inclus des mots-cles SEO naturellement
- Cree un sentiment d'urgence sans etre agressif
- Prix en .99 ou .95 pour l'effet psychologique"""

    def get_tools(self) -> list[dict]:
        return [
            {
                "name": "generate_product_listing",
                "description": "Genere le titre et la description optimises pour un produit.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "product_title": {"type": "string"},
                        "product_info": {"type": "string"},
                        "target_audience": {"type": "string"},
                        "niche": {"type": "string"},
                    },
                    "required": ["product_title", "product_info"],
                },
            },
            {
                "name": "set_optimal_price",
                "description": "Determine le prix de vente optimal.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "cost_price": {"type": "number"},
                        "competitor_avg_price": {"type": "number"},
                        "perceived_value": {
                            "type": "string",
                            "enum": ["budget", "mid-range", "premium"],
                        },
                    },
                    "required": ["cost_price"],
                },
            },
            {
                "name": "publish_to_shopify",
                "description": "Publie le produit sur la boutique Shopify.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "store_id": {"type": "string"},
                        "title": {"type": "string"},
                        "description_html": {"type": "string"},
                        "price": {"type": "number"},
                        "images": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["store_id", "title", "description_html", "price"],
                },
            },
        ]

    def execute_tool(self, tool_name: str, tool_input: dict) -> str:
        if tool_name == "generate_product_listing":
            return json.dumps({
                "title": tool_input["product_title"],
                "note": "The agent (Claude) generates the actual copy in its reasoning",
            })

        elif tool_name == "set_optimal_price":
            cost = tool_input["cost_price"]
            competitor = tool_input.get("competitor_avg_price", cost * 3)
            markup = {"budget": 2.0, "mid-range": 2.5, "premium": 3.5}
            factor = markup.get(tool_input.get("perceived_value", "mid-range"), 2.5)
            suggested = round(cost * factor, 2)
            # Apply psychological pricing
            suggested = int(suggested) + 0.99
            return json.dumps({
                "cost_price": cost,
                "suggested_price": suggested,
                "competitor_avg": competitor,
                "margin_percent": round(((suggested - cost) / suggested) * 100, 1),
            })

        elif tool_name == "publish_to_shopify":
            # TODO: Implement via Shopify GraphQL API
            return json.dumps({
                "status": "placeholder",
                "store_id": tool_input["store_id"],
                "title": tool_input["title"],
                "message": "Product will be published via Shopify GraphQL API",
            })

        return json.dumps({"error": f"Unknown tool: {tool_name}"})
