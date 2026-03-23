"""
Customer Service Agent - Handles customer support autonomously.
"""

import json

from app.agents.base import BaseAgent


class CustomerServiceAgent(BaseAgent):
    agent_type = "customer_service"

    def get_system_prompt(self) -> str:
        return """Tu es un agent de service client expert et empathique.

Ton objectif : resoudre les problemes clients de maniere autonome.

Regles :
- Toujours etre poli et empathique
- Repondre rapidement et precisement
- Si le probleme est un retard de livraison : verifier le suivi et rassurer
- Si le probleme est un produit defectueux : proposer remboursement ou renvoi
- Si le client demande un remboursement : l'accorder si < 30 jours et < 50 EUR
- Pour les montants > 50 EUR ou situations complexes : escalader vers l'humain

Reponds toujours en francais sauf si le client ecrit dans une autre langue."""

    def get_tools(self) -> list[dict]:
        return [
            {
                "name": "get_customer_info",
                "description": "Recupere les informations du client et son historique.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "customer_email": {"type": "string"},
                    },
                    "required": ["customer_email"],
                },
            },
            {
                "name": "get_order_details",
                "description": "Recupere les details d'une commande specifique.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string"},
                    },
                    "required": ["order_id"],
                },
            },
            {
                "name": "send_reply",
                "description": "Envoie une reponse au client.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "conversation_id": {"type": "string"},
                        "message": {"type": "string"},
                    },
                    "required": ["conversation_id", "message"],
                },
            },
            {
                "name": "process_refund",
                "description": "Traite un remboursement pour une commande.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string"},
                        "amount": {"type": "number"},
                        "reason": {"type": "string"},
                    },
                    "required": ["order_id", "amount", "reason"],
                },
            },
            {
                "name": "escalate_to_human",
                "description": "Escalade la conversation vers un humain.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "conversation_id": {"type": "string"},
                        "reason": {"type": "string"},
                    },
                    "required": ["conversation_id", "reason"],
                },
            },
        ]

    def execute_tool(self, tool_name: str, tool_input: dict) -> str:
        if tool_name == "get_customer_info":
            # TODO: Query from database
            return json.dumps({
                "email": tool_input["customer_email"],
                "total_orders": 0,
                "total_spent": 0,
                "note": "Placeholder",
            })

        elif tool_name == "get_order_details":
            return json.dumps({
                "order_id": tool_input["order_id"],
                "status": "processing",
                "note": "Placeholder",
            })

        elif tool_name == "send_reply":
            # TODO: Send via email/Shopify
            return json.dumps({
                "sent": True,
                "conversation_id": tool_input["conversation_id"],
                "note": "Placeholder",
            })

        elif tool_name == "process_refund":
            # TODO: Process via Shopify Payments API
            return json.dumps({
                "refunded": True,
                "amount": tool_input["amount"],
                "note": "Placeholder - will use Shopify Payments API",
            })

        elif tool_name == "escalate_to_human":
            return json.dumps({
                "escalated": True,
                "conversation_id": tool_input["conversation_id"],
                "reason": tool_input["reason"],
            })

        return json.dumps({"error": f"Unknown tool: {tool_name}"})
