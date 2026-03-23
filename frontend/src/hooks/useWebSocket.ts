"use client";

import { useState, useEffect, useRef, useCallback } from "react";

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";

interface WSEvent {
  type: string;
  data: Record<string, unknown>;
  timestamp: string;
}

export function useWebSocket() {
  const [events, setEvents] = useState<WSEvent[]>([]);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeout = useRef<NodeJS.Timeout>(undefined);

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(`${WS_URL}/ws/dashboard`);

      ws.onopen = () => {
        setConnected(true);
        // Send periodic pings
        const ping = setInterval(() => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send("ping");
          }
        }, 30000);
        ws.addEventListener("close", () => clearInterval(ping));
      };

      ws.onmessage = (event) => {
        if (event.data === "pong") return;
        try {
          const parsed = JSON.parse(event.data) as WSEvent;
          setEvents((prev) => [parsed, ...prev].slice(0, 100));
        } catch {
          // ignore non-JSON messages
        }
      };

      ws.onclose = () => {
        setConnected(false);
        // Reconnect after 5 seconds
        reconnectTimeout.current = setTimeout(connect, 5000);
      };

      ws.onerror = () => {
        ws.close();
      };

      wsRef.current = ws;
    } catch {
      // WebSocket not available
      reconnectTimeout.current = setTimeout(connect, 5000);
    }
  }, []);

  useEffect(() => {
    connect();
    return () => {
      wsRef.current?.close();
      if (reconnectTimeout.current) clearTimeout(reconnectTimeout.current);
    };
  }, [connect]);

  return { events, connected };
}
