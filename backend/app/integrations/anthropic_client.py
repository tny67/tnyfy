"""
Anthropic Claude API client wrapper for Tnyfy.
"""

import anthropic

from app.config import settings


def get_anthropic_client() -> anthropic.Anthropic:
    """Get a configured Anthropic client."""
    return anthropic.Anthropic(api_key=settings.anthropic_api_key)
