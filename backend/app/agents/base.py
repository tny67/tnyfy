"""
BaseAgent - The core of Tnyfy's AI system.

Each agent runs an autonomous loop with Claude API:
1. Send message to Claude with system prompt + tools
2. If Claude calls a tool -> execute it -> feed result back
3. Repeat until Claude returns a final text response
4. Log every iteration (tokens, cost, duration)
"""

import time
import uuid
from abc import ABC, abstractmethod
from datetime import datetime

import anthropic

from app.config import settings


class AgentResult:
    def __init__(self, success: bool, output: str, data: dict | None = None):
        self.success = success
        self.output = output
        self.data = data or {}
        self.total_tokens = 0
        self.total_cost = 0.0
        self.duration_ms = 0


class BaseAgent(ABC):
    """Abstract base class for all Tnyfy AI agents."""

    agent_type: str = "base"
    max_iterations: int = 30
    max_cost_per_run: float = 3.00
    model: str = "claude-sonnet-4-20250514"

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.run_id = str(uuid.uuid4())
        self.iterations = 0
        self.total_tokens = 0
        self.total_cost = 0.0

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        ...

    @abstractmethod
    def get_tools(self) -> list[dict]:
        """Return the list of tools available to this agent."""
        ...

    @abstractmethod
    def execute_tool(self, tool_name: str, tool_input: dict) -> str:
        """Execute a tool and return the result as a string."""
        ...

    def run(self, task: str, context: dict | None = None) -> AgentResult:
        """Run the agent loop for a given task."""
        start_time = time.time()

        system_prompt = self.get_system_prompt()
        if context:
            system_prompt += f"\n\nContexte actuel:\n{self._format_context(context)}"

        tools = self.get_tools()
        messages = [{"role": "user", "content": task}]

        try:
            result = self._agent_loop(system_prompt, tools, messages)
            result.duration_ms = int((time.time() - start_time) * 1000)
            return result
        except Exception as e:
            return AgentResult(
                success=False,
                output=f"Agent error: {str(e)}",
            )

    def _agent_loop(
        self,
        system_prompt: str,
        tools: list[dict],
        messages: list[dict],
    ) -> AgentResult:
        """The core agent loop - send to Claude, execute tools, repeat."""

        while self.iterations < self.max_iterations:
            self.iterations += 1

            # Check cost limit
            if self.total_cost >= self.max_cost_per_run:
                return AgentResult(
                    success=False,
                    output=f"Cost limit reached: ${self.total_cost:.4f}",
                )

            # Call Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                tools=tools if tools else anthropic.NOT_GIVEN,
                messages=messages,
            )

            # Track usage
            self._track_usage(response.usage)

            # Check stop reason
            if response.stop_reason == "end_turn":
                # Agent is done - extract final text
                final_text = ""
                for block in response.content:
                    if block.type == "text":
                        final_text += block.text
                return AgentResult(success=True, output=final_text)

            if response.stop_reason == "tool_use":
                # Process tool calls
                assistant_content = response.content
                messages.append({"role": "assistant", "content": assistant_content})

                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        try:
                            result = self.execute_tool(block.name, block.input)
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": str(result),
                            })
                        except Exception as e:
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": f"Error: {str(e)}",
                                "is_error": True,
                            })

                messages.append({"role": "user", "content": tool_results})
            else:
                # Unexpected stop reason
                return AgentResult(
                    success=False,
                    output=f"Unexpected stop reason: {response.stop_reason}",
                )

        return AgentResult(
            success=False,
            output=f"Max iterations ({self.max_iterations}) reached",
        )

    def _track_usage(self, usage):
        """Track token usage and estimate cost."""
        input_tokens = usage.input_tokens
        output_tokens = usage.output_tokens
        self.total_tokens += input_tokens + output_tokens
        # Sonnet pricing: $3/1M input, $15/1M output
        self.total_cost += (input_tokens * 3 + output_tokens * 15) / 1_000_000

    def _format_context(self, context: dict) -> str:
        """Format context dict into readable string."""
        return "\n".join(f"- {k}: {v}" for k, v in context.items())

    def to_log_dict(self) -> dict:
        """Return data for agent_logs table."""
        return {
            "agent_type": self.agent_type,
            "tokens_used": self.total_tokens,
            "cost_usd": round(self.total_cost, 4),
        }
