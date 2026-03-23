"""
Order Manager Agent - Handles orders and fulfillment automatically.
"""

import json

from app.agents.base import BaseAgent


class OrderManagerAgent(BaseAgent):
    agent_type = "order_manager"

    def get_system_prompt(self) -> str:
        return """Tu es un gestionnaire de commandes e-commerce expert.

Ton objectif : traiter les commandes automatiquement.

Pour chaque nouvelle commande :
1. Verifie les details (produit, quantite, adresse)
2. Passe la commande au fournisseur (AliExpress/supplier)
3. Met a jour le statut de la commande
4. Envoie les infos de suivi au client

Gere aussi les annulations et remboursements."""

    def get_tools(self) -> list[dict]:
        return [
            {
                "name": "get_pending_orders",
                "description": "Recupere les commandes en attente de traitement.",
                "input_schema": {
                    "type": "object",
                    "properties": {"store_id": {"type": "string"}},
                    "required": ["store_id"],
                },
            },
            {
                "name": "place_supplier_order",
                "description": "Passe la commande chez le fournisseur.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string"},
                        "supplier_url": {"type": "string"},
                        "shipping_address": {"type": "object"},
                    },
                    "required": ["order_id", "supplier_url"],
                },
            },
            {
                "name": "update_order_status",
                "description": "Met a jour le statut d'une commande.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string"},
                        "status": {
                            "type": "string",
                            "enum": ["processing", "fulfilled", "cancelled", "refunded"],
                        },
                        "tracking_number": {"type": "string"},
                    },
                    "required": ["order_id", "status"],
                },
            },
            {
                "name": "send_customer_notification",
                "description": "Envoie une notification au client.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "customer_email": {"type": "string"},
                        "subject": {"type": "string"},
                        "message": {"type": "string"},
                    },
                    "required": ["customer_email", "subject", "message"],
                },
            },
        ]

    def execute_tool(self, tool_name: str, tool_input: dict) -> str:
        if tool_name == "get_pending_orders":
            # TODO: Query from database
            return json.dumps({"orders": [], "note": "No pending orders"})

        elif tool_name == "place_supplier_order":
            # TODO: Automate supplier ordering
            return json.dumps({
                "status": "placeholder",
                "order_id": tool_input["order_id"],
                "message": "Supplier order automation not yet implemented",
            })

        elif tool_name == "update_order_status":
            # TODO: Update in DB and Shopify
            return json.dumps({
                "order_id": tool_input["order_id"],
                "new_status": tool_input["status"],
                "note": "Placeholder",
            })

        elif tool_name == "send_customer_notification":
            # TODO: Send email via SMTP or Shopify
            return json.dumps({
                "sent_to": tool_input["customer_email"],
                "subject": tool_input["subject"],
                "note": "Placeholder - email sending not yet implemented",
            })

        return json.dumps({"error": f"Unknown tool: {tool_name}"})
