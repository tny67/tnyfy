from datetime import datetime

from pydantic import BaseModel


class AgentStatusOut(BaseModel):
    agent_type: str
    status: str
    last_run: datetime | None = None
    total_runs: int = 0
    total_cost: float = 0.0


class AgentLogOut(BaseModel):
    id: str
    store_id: str | None
    agent_type: str
    action: str
    status: str
    tokens_used: int
    cost_usd: float
    duration_ms: int
    created_at: datetime

    model_config = {"from_attributes": True}
