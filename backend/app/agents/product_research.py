"""
Product Research Agent - Finds winning products for e-commerce.

Uses Claude to analyze trends, competition, and margins to score products.
"""

import json

from app.agents.base import BaseAgent


class ProductResearchAgent(BaseAgent):
    agent_type = "product_research"

    def __init__(self, store_id: str | None = None):
        super().__init__()
        self.store_id = store_id
        self.found_products: list[dict] = []

    def get_system_prompt(self) -> str:
        return """Tu es un expert en recherche de produits e-commerce pour le dropshipping.

Ton objectif : trouver des produits gagnants avec un fort potentiel de vente.

Criteres d'evaluation (score sur 100) :
- Tendance montante (Google Trends) : 25 points
- Marge beneficiaire > 60% : 25 points
- Concurrence faible/moyenne : 20 points
- Potentiel viral (visuel, wow factor) : 15 points
- Facilite de livraison (leger, pas fragile) : 15 points

Pour chaque produit trouve, tu dois :
1. Rechercher les tendances avec search_trends
2. Trouver des fournisseurs avec search_suppliers
3. Analyser la concurrence avec analyze_competition
4. Calculer la marge avec calculate_margin
5. Sauvegarder le produit avec save_product si le score > 60

Trouve au minimum 5 produits scores. Sois precis dans tes analyses."""

    def get_tools(self) -> list[dict]:
        return [
            {
                "name": "search_trends",
                "description": "Recherche les tendances Google pour un terme. Retourne un score de tendance de 0 a 100.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Le terme de recherche",
                        },
                        "region": {
                            "type": "string",
                            "description": "Region (FR, US, etc.)",
                            "default": "FR",
                        },
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "search_suppliers",
                "description": "Cherche des fournisseurs/produits sur AliExpress. Retourne prix, avis, et nombre de commandes.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Recherche produit",
                        },
                        "sort_by": {
                            "type": "string",
                            "enum": ["orders", "price_low", "rating"],
                            "default": "orders",
                        },
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "analyze_competition",
                "description": "Analyse la concurrence pour un type de produit. Retourne le nombre de boutiques concurrentes et leurs prix moyens.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "product_query": {
                            "type": "string",
                            "description": "Le type de produit a analyser",
                        },
                    },
                    "required": ["product_query"],
                },
            },
            {
                "name": "calculate_margin",
                "description": "Calcule la marge beneficiaire d'un produit.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "cost_price": {
                            "type": "number",
                            "description": "Prix d'achat fournisseur en EUR",
                        },
                        "selling_price": {
                            "type": "number",
                            "description": "Prix de vente suggere en EUR",
                        },
                        "shipping_cost": {
                            "type": "number",
                            "description": "Cout d'expedition en EUR",
                            "default": 0,
                        },
                    },
                    "required": ["cost_price", "selling_price"],
                },
            },
            {
                "name": "save_product",
                "description": "Sauvegarde un produit recherche dans la base de donnees.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "cost_price": {"type": "number"},
                        "selling_price": {"type": "number"},
                        "supplier_url": {"type": "string"},
                        "research_score": {
                            "type": "number",
                            "description": "Score de 0 a 100",
                        },
                        "research_notes": {
                            "type": "string",
                            "description": "Notes d'analyse",
                        },
                    },
                    "required": ["title", "cost_price", "selling_price", "research_score"],
                },
            },
        ]

    def execute_tool(self, tool_name: str, tool_input: dict) -> str:
        """Execute product research tools."""
        if tool_name == "search_trends":
            # TODO: Integrate with Google Trends API (pytrends) or SerpAPI
            return json.dumps({
                "query": tool_input["query"],
                "trend_score": 72,
                "trend_direction": "rising",
                "related_queries": [
                    f"{tool_input['query']} 2026",
                    f"best {tool_input['query']}",
                ],
                "note": "Placeholder - integrate with Google Trends API",
            })

        elif tool_name == "search_suppliers":
            # TODO: Integrate with AliExpress API or web scraping
            return json.dumps({
                "query": tool_input["query"],
                "results": [
                    {
                        "title": f"{tool_input['query']} - Best Seller",
                        "price_usd": 8.50,
                        "rating": 4.7,
                        "orders": 15000,
                        "shipping": "Free ePacket",
                    }
                ],
                "note": "Placeholder - integrate with supplier APIs",
            })

        elif tool_name == "analyze_competition":
            # TODO: Analyze Shopify stores selling similar products
            return json.dumps({
                "product_query": tool_input["product_query"],
                "competitors_found": 12,
                "avg_price": 29.99,
                "price_range": {"min": 19.99, "max": 49.99},
                "competition_level": "medium",
                "note": "Placeholder - integrate with competition analysis",
            })

        elif tool_name == "calculate_margin":
            cost = tool_input["cost_price"]
            sell = tool_input["selling_price"]
            ship = tool_input.get("shipping_cost", 0)
            total_cost = cost + ship
            profit = sell - total_cost
            margin_pct = (profit / sell) * 100 if sell > 0 else 0
            return json.dumps({
                "cost_price": cost,
                "shipping_cost": ship,
                "total_cost": total_cost,
                "selling_price": sell,
                "profit_per_unit": round(profit, 2),
                "margin_percent": round(margin_pct, 1),
            })

        elif tool_name == "save_product":
            product = {
                "title": tool_input["title"],
                "description": tool_input.get("description", ""),
                "cost_price": tool_input["cost_price"],
                "price": tool_input["selling_price"],
                "supplier_url": tool_input.get("supplier_url", ""),
                "research_score": tool_input["research_score"],
                "research_data": {"notes": tool_input.get("research_notes", "")},
                "status": "researched",
            }
            self.found_products.append(product)
            # TODO: Save to database via service layer
            return json.dumps({
                "saved": True,
                "product_count": len(self.found_products),
                "title": product["title"],
            })

        return json.dumps({"error": f"Unknown tool: {tool_name}"})
