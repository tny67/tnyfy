"""
Settings API - Initial configuration endpoint.
The user configures credentials once, Tnyfy handles the rest.
"""

import os

from fastapi import APIRouter
from pydantic import BaseModel

from app.config import settings

router = APIRouter()


class SettingsUpdate(BaseModel):
    shopify_partner_email: str | None = None
    shopify_partner_password: str | None = None
    anthropic_api_key: str | None = None
    daily_budget: float | None = None
    max_stores: int | None = None


class SettingsOut(BaseModel):
    shopify_partner_email: str
    has_shopify_password: bool
    has_anthropic_key: bool
    daily_budget: float
    max_stores: int
    system_ready: bool


@router.get("/", response_model=SettingsOut)
async def get_settings():
    return SettingsOut(
        shopify_partner_email=settings.shopify_partner_email,
        has_shopify_password=bool(settings.shopify_partner_password),
        has_anthropic_key=bool(settings.anthropic_api_key),
        daily_budget=settings.agent_daily_budget,
        max_stores=5,
        system_ready=bool(settings.anthropic_api_key and settings.shopify_partner_email),
    )


@router.post("/", response_model=SettingsOut)
async def update_settings(data: SettingsUpdate):
    """Update settings by writing to .env file."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), ".env")

    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key] = value

    if data.shopify_partner_email is not None:
        env_vars["SHOPIFY_PARTNER_EMAIL"] = data.shopify_partner_email
    if data.shopify_partner_password is not None:
        env_vars["SHOPIFY_PARTNER_PASSWORD"] = data.shopify_partner_password
    if data.anthropic_api_key is not None:
        env_vars["ANTHROPIC_API_KEY"] = data.anthropic_api_key
    if data.daily_budget is not None:
        env_vars["AGENT_DAILY_BUDGET"] = str(data.daily_budget)

    with open(env_path, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")

    return SettingsOut(
        shopify_partner_email=env_vars.get("SHOPIFY_PARTNER_EMAIL", ""),
        has_shopify_password=bool(env_vars.get("SHOPIFY_PARTNER_PASSWORD")),
        has_anthropic_key=bool(env_vars.get("ANTHROPIC_API_KEY")),
        daily_budget=float(env_vars.get("AGENT_DAILY_BUDGET", "50.0")),
        max_stores=int(env_vars.get("MAX_STORES", "5")),
        system_ready=bool(env_vars.get("ANTHROPIC_API_KEY") and env_vars.get("SHOPIFY_PARTNER_EMAIL")),
    )
