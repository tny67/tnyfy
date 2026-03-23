"""
Store Creator Agent - Creates Shopify stores automatically via Playwright.

Uses browser automation to create stores on Shopify Partner Dashboard.
"""

import json

from app.agents.base import BaseAgent


class StoreCreatorAgent(BaseAgent):
    agent_type = "store_creator"

    def get_system_prompt(self) -> str:
        return """Tu es un expert en creation de boutiques Shopify.

Ton objectif : creer une nouvelle boutique Shopify optimisee pour une niche specifique.

Etapes :
1. Creer la boutique via le Shopify Partner Dashboard (automation navigateur)
2. Generer un nom de marque accrocheur pour la niche
3. Configurer le theme et le design
4. Mettre en place les pages essentielles (About, Contact, Politique de retour)
5. Configurer les methodes de paiement et d'expedition

Sois methodique et assure-toi que chaque etape est validee avant de passer a la suivante."""

    def get_tools(self) -> list[dict]:
        return [
            {
                "name": "generate_brand_name",
                "description": "Genere un nom de marque pour une niche donnee.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "niche": {"type": "string"},
                        "style": {
                            "type": "string",
                            "enum": ["modern", "luxury", "fun", "minimal"],
                            "default": "modern",
                        },
                    },
                    "required": ["niche"],
                },
            },
            {
                "name": "create_shopify_store",
                "description": "Cree une boutique Shopify via le Partner Dashboard avec Playwright.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "store_name": {"type": "string"},
                        "niche": {"type": "string"},
                    },
                    "required": ["store_name", "niche"],
                },
            },
            {
                "name": "configure_store_theme",
                "description": "Configure le theme de la boutique.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "store_domain": {"type": "string"},
                        "color_scheme": {
                            "type": "string",
                            "enum": ["dark", "light", "colorful"],
                        },
                    },
                    "required": ["store_domain"],
                },
            },
            {
                "name": "setup_store_pages",
                "description": "Cree les pages essentielles de la boutique.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "store_domain": {"type": "string"},
                        "brand_name": {"type": "string"},
                        "niche": {"type": "string"},
                    },
                    "required": ["store_domain", "brand_name"],
                },
            },
        ]

    def execute_tool(self, tool_name: str, tool_input: dict) -> str:
        if tool_name == "generate_brand_name":
            # The agent itself (Claude) generates the brand name via reasoning
            return json.dumps({
                "suggestions": [
                    f"{tool_input['niche'].title()}Lab",
                    f"The{tool_input['niche'].title()}Co",
                    f"{tool_input['niche'].title()}Store",
                ],
                "note": "Choose or modify one of these suggestions",
            })

        elif tool_name == "create_shopify_store":
            # TODO: Implement Playwright automation
            return json.dumps({
                "status": "placeholder",
                "store_name": tool_input["store_name"],
                "message": "Playwright automation not yet implemented. Will create store via Shopify Partner Dashboard.",
                "next_steps": [
                    "Navigate to partners.shopify.com",
                    "Login with credentials",
                    "Create development store",
                    "Get API credentials",
                ],
            })

        elif tool_name == "configure_store_theme":
            return json.dumps({
                "status": "placeholder",
                "message": "Theme configuration will be done via Shopify API once store is created.",
            })

        elif tool_name == "setup_store_pages":
            return json.dumps({
                "status": "placeholder",
                "pages_to_create": [
                    "About Us",
                    "Contact",
                    "Shipping Policy",
                    "Return Policy",
                    "Privacy Policy",
                    "Terms of Service",
                ],
                "message": "Pages will be created via Shopify API with AI-generated content.",
            })

        return json.dumps({"error": f"Unknown tool: {tool_name}"})
