from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://tnyfy:tnyfy_dev_2024@localhost:5432/tnyfy"
    redis_url: str = "redis://localhost:6379/0"

    # Security
    secret_key: str = "change-me-to-a-random-string"

    # Anthropic
    anthropic_api_key: str = ""

    # Shopify Partner
    shopify_partner_email: str = ""
    shopify_partner_password: str = ""

    # Agent limits
    agent_max_cost_per_run: float = 3.00
    agent_daily_budget: float = 50.00
    agent_max_iterations: int = 30
    agent_timeout_seconds: int = 600

    # CORS
    cors_origins: str = "http://localhost:3000"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
