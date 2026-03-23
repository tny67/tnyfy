"""
Niche Finder Agent - Discovers profitable e-commerce niches.

Analyzes market trends to find untapped niches with high profit potential.
"""

import json

from app.agents.base import BaseAgent


class NicheFinderAgent(BaseAgent):
    agent_type = "niche_finder"

    def __init__(self):
        super().__init__()
        self.found_niches: list[dict] = []

    def get_system_prompt(self) -> str:
        return """Tu es un expert en analyse de marche e-commerce.

Ton objectif : trouver des niches rentables pour le dropshipping/e-commerce.

Criteres d'une bonne niche :
- Demande croissante (tendance montante)
- Concurrence pas trop elevee
- Marge potentielle > 50%
- Produits entre 20 et 100 EUR
- Public cible identifiable (publicite facile)
- Pas de problemes legaux/reglementaires

Utilise les outils disponibles pour analyser les tendances et evaluer les niches.
Propose au minimum 3 niches scorees et justifie tes choix."""

    def get_tools(self) -> list[dict]:
        return [
            {
                "name": "search_trending_niches",
                "description": "Recherche les niches en tendance sur Google Trends, TikTok, et Amazon.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "Categorie large (beaute, tech, maison, sport, etc.)",
                        },
                        "region": {
                            "type": "string",
                            "default": "FR",
                        },
                    },
                    "required": ["category"],
                },
            },
            {
                "name": "evaluate_niche",
                "description": "Evalue le potentiel d'une niche specifique.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "niche_name": {"type": "string"},
                        "target_audience": {"type": "string"},
                    },
                    "required": ["niche_name"],
                },
            },
            {
                "name": "save_niche",
                "description": "Sauvegarde une niche evaluee pour lancement potentiel.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "niche_name": {"type": "string"},
                        "score": {
                            "type": "number",
                            "description": "Score de 0 a 100",
                        },
                        "target_audience": {"type": "string"},
                        "avg_product_price": {"type": "number"},
                        "reasoning": {"type": "string"},
                    },
                    "required": ["niche_name", "score", "reasoning"],
                },
            },
        ]

    def execute_tool(self, tool_name: str, tool_input: dict) -> str:
        if tool_name == "search_trending_niches":
            # TODO: Integrate with trend APIs
            return json.dumps({
                "category": tool_input["category"],
                "trending_niches": [
                    {"name": "LED therapy masks", "growth": "+180%"},
                    {"name": "Portable blenders", "growth": "+95%"},
                    {"name": "Posture correctors", "growth": "+120%"},
                ],
                "note": "Placeholder - integrate with trend APIs",
            })

        elif tool_name == "evaluate_niche":
            return json.dumps({
                "niche": tool_input["niche_name"],
                "demand_score": 78,
                "competition_score": 45,
                "margin_potential": "65-75%",
                "market_size_estimate": "Growing market",
                "note": "Placeholder - integrate with market analysis",
            })

        elif tool_name == "save_niche":
            niche = {
                "name": tool_input["niche_name"],
                "score": tool_input["score"],
                "target_audience": tool_input.get("target_audience", ""),
                "reasoning": tool_input["reasoning"],
            }
            self.found_niches.append(niche)
            return json.dumps({"saved": True, "niche": niche["name"]})

        return json.dumps({"error": f"Unknown tool: {tool_name}"})
