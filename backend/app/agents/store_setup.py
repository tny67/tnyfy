"""
Store Setup Agent - Configures existing Shopify stores via API.
"""

import json

from app.agents.base import BaseAgent


class StoreSetupAgent(BaseAgent):
    agent_type = "store_setup"

    def get_system_prompt(self) -> str:
        return """Tu es un expert en configuration de boutiques Shopify.

Tu configures une boutique deja creee pour la rendre prete a vendre.
Utilise l'API Shopify pour configurer :
- Collections de produits
- Methodes d'expedition
- Politiques de la boutique
- Parametres SEO

Verifie que tout est correct avant de marquer la boutique comme 'active'."""

    def get_tools(self) -> list[dict]:
        return [
            {
                "name": "get_store_info",
                "description": "Recupere les infos actuelles de la boutique Shopify.",
                "input_schema": {
                    "type": "object",
                    "properties": {"store_domain": {"type": "string"}},
                    "required": ["store_domain"],
                },
            },
            {
                "name": "create_collections",
                "description": "Cree des collections de produits.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "collections": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["collections"],
                },
            },
            {
                "name": "configure_shipping",
                "description": "Configure les zones et tarifs d'expedition.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "free_shipping_threshold": {"type": "number"},
                        "standard_rate": {"type": "number"},
                    },
                    "required": ["free_shipping_threshold"],
                },
            },
            {
                "name": "mark_store_active",
                "description": "Marque la boutique comme active et prete a vendre.",
                "input_schema": {
                    "type": "object",
                    "properties": {"store_id": {"type": "string"}},
                    "required": ["store_id"],
                },
            },
        ]

    def execute_tool(self, tool_name: str, tool_input: dict) -> str:
        if tool_name == "get_store_info":
            return json.dumps({
                "domain": tool_input["store_domain"],
                "status": "setup",
                "note": "Placeholder - will use Shopify GraphQL API",
            })

        elif tool_name == "create_collections":
            return json.dumps({
                "created": tool_input["collections"],
                "note": "Placeholder - will use Shopify API",
            })

        elif tool_name == "configure_shipping":
            return json.dumps({
                "free_above": tool_input["free_shipping_threshold"],
                "standard": tool_input.get("standard_rate", 4.99),
                "note": "Placeholder - will use Shopify API",
            })

        elif tool_name == "mark_store_active":
            return json.dumps({"store_id": tool_input["store_id"], "status": "active"})

        return json.dumps({"error": f"Unknown tool: {tool_name}"})
