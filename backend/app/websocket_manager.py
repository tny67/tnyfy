"""
WebSocket connection manager for real-time dashboard updates.

Broadcasts events to all connected dashboard clients:
- New orders
- Agent activity
- Store status changes
- Alerts
"""

import json
import logging
from datetime import datetime

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class WebSocketManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Dashboard client connected ({len(self.active_connections)} total)")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Dashboard client disconnected ({len(self.active_connections)} total)")

    async def broadcast(self, event_type: str, data: dict):
        """Broadcast an event to all connected dashboard clients."""
        message = json.dumps({
            "type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
        })
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                disconnected.append(connection)

        for conn in disconnected:
            self.active_connections.remove(conn)

    async def send_agent_event(self, agent_type: str, action: str, status: str, store_id: str | None = None):
        await self.broadcast("agent_event", {
            "agent_type": agent_type,
            "action": action,
            "status": status,
            "store_id": store_id,
        })

    async def send_new_order(self, order_data: dict):
        await self.broadcast("new_order", order_data)

    async def send_store_update(self, store_id: str, status: str):
        await self.broadcast("store_update", {
            "store_id": store_id,
            "status": status,
        })

    async def send_alert(self, level: str, message: str):
        await self.broadcast("alert", {
            "level": level,
            "message": message,
        })


ws_manager = WebSocketManager()
