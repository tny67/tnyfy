"use client";

import { useApi } from "@/hooks/useApi";
import type { AgentLog } from "@/types/store";

interface WSEvent {
  type: string;
  data: Record<string, unknown>;
  timestamp: string;
}

const agentTypeLabels: Record<string, string> = {
  orchestrator: "Orchestrator",
  niche_finder: "Niche Finder",
  store_creator: "Store Creator",
  store_setup: "Store Setup",
  product_research: "Product Research",
  listing_agent: "Listing Agent",
  order_manager: "Order Manager",
  customer_service: "Customer Service",
};

const statusColors: Record<string, string> = {
  idle: "var(--text-secondary)",
  started: "var(--warning)",
  running: "var(--accent)",
  completed: "var(--success)",
  failed: "var(--danger)",
};

export function AgentActivityFeed({ liveEvents }: { liveEvents?: WSEvent[] }) {
  const { data: logs } = useApi<AgentLog[]>("/api/v1/agents/logs?limit=10", 15000);

  const agentEvents = (liveEvents || []).filter((e) => e.type === "agent_event");

  return (
    <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-5">
      <h3 className="text-sm font-medium text-[var(--text-secondary)] mb-4">
        Agents IA - Activite
      </h3>
      <div className="space-y-3">
        {/* Live events first */}
        {agentEvents.slice(0, 5).map((event, i) => (
          <div key={`live-${i}`} className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full animate-pulse" style={{ backgroundColor: "var(--accent)" }} />
              <span className="text-xs">
                {agentTypeLabels[event.data.agent_type as string] || event.data.agent_type as string}
              </span>
            </div>
            <span className="text-xs text-[var(--text-secondary)] truncate max-w-[120px]">
              {event.data.action as string}
            </span>
          </div>
        ))}

        {/* Historical logs */}
        {(logs || []).slice(0, agentEvents.length > 0 ? 5 : 10).map((log) => (
          <div key={log.id} className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-2">
              <div
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: statusColors[log.status] || "var(--text-secondary)" }}
              />
              <span className="text-xs">
                {agentTypeLabels[log.agent_type] || log.agent_type}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-[var(--text-secondary)] truncate max-w-[100px]">
                {log.action}
              </span>
              {log.cost_usd > 0 && (
                <span className="text-xs text-[var(--text-secondary)]">
                  ${log.cost_usd.toFixed(3)}
                </span>
              )}
            </div>
          </div>
        ))}

        {!logs?.length && !agentEvents.length && (
          <div className="text-center py-4 text-[var(--text-secondary)] text-xs">
            En attente du premier cycle...
          </div>
        )}
      </div>
    </div>
  );
}
