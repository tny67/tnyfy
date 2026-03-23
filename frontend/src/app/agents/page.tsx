"use client";

import { useApi } from "@/hooks/useApi";
import type { AgentLog } from "@/types/store";

interface AgentStatus {
  agent_type: string;
  status: string;
  last_run: string | null;
  total_runs: number;
  total_cost: number;
}

const agentLabels: Record<string, string> = {
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

export default function AgentsPage() {
  const { data: statuses } = useApi<AgentStatus[]>("/api/v1/agents/status", 10000);
  const { data: logs } = useApi<AgentLog[]>("/api/v1/agents/logs?limit=30", 10000);

  const totalCost = statuses?.reduce((sum, s) => sum + s.total_cost, 0) ?? 0;
  const todayLogs = logs?.filter((l) => {
    const today = new Date().toISOString().split("T")[0];
    return l.created_at.startsWith(today);
  });
  const todayCost = todayLogs?.reduce((sum, l) => sum + l.cost_usd, 0) ?? 0;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Agents IA</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Agent statuses */}
        <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-5">
          <h3 className="text-sm font-medium text-[var(--text-secondary)] mb-4">Statut des agents</h3>
          <div className="space-y-3">
            {(statuses || []).map((agent) => (
              <div key={agent.agent_type} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <div
                    className="w-2 h-2 rounded-full"
                    style={{ backgroundColor: statusColors[agent.status] || "var(--text-secondary)" }}
                  />
                  <span>{agentLabels[agent.agent_type] || agent.agent_type}</span>
                </div>
                <div className="flex items-center gap-3 text-xs text-[var(--text-secondary)]">
                  <span>{agent.total_runs} runs</span>
                  <span>${agent.total_cost.toFixed(3)}</span>
                  <span className="bg-[var(--bg-secondary)] px-2 py-0.5 rounded">{agent.status}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Cost tracker */}
        <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-5">
          <h3 className="text-sm font-medium text-[var(--text-secondary)] mb-4">Cout IA</h3>
          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-[var(--text-secondary)]">Aujourd&apos;hui</span>
              <span>${todayCost.toFixed(3)}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-[var(--text-secondary)]">Total historique</span>
              <span>${totalCost.toFixed(3)}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-[var(--text-secondary)]">Budget max/jour</span>
              <span>$50.00</span>
            </div>
            <div className="w-full bg-[var(--bg-secondary)] rounded-full h-2 mt-2">
              <div
                className="bg-[var(--accent)] h-2 rounded-full transition-all"
                style={{ width: `${Math.min((todayCost / 50) * 100, 100)}%` }}
              />
            </div>
            <p className="text-xs text-[var(--text-secondary)] text-right">
              {((todayCost / 50) * 100).toFixed(1)}% du budget utilise
            </p>
          </div>
        </div>
      </div>

      {/* Activity log */}
      <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-5">
        <h3 className="text-sm font-medium text-[var(--text-secondary)] mb-4">
          Historique des actions ({logs?.length ?? 0})
        </h3>
        {logs && logs.length > 0 ? (
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {logs.map((log) => (
              <div key={log.id} className="flex items-center justify-between text-xs py-1.5 border-b border-[var(--border)] last:border-0">
                <div className="flex items-center gap-2">
                  <div
                    className="w-1.5 h-1.5 rounded-full"
                    style={{ backgroundColor: statusColors[log.status] || "var(--text-secondary)" }}
                  />
                  <span className="font-medium">{agentLabels[log.agent_type] || log.agent_type}</span>
                  <span className="text-[var(--text-secondary)]">{log.action}</span>
                </div>
                <div className="flex items-center gap-3 text-[var(--text-secondary)]">
                  <span>{log.tokens_used} tokens</span>
                  <span>${log.cost_usd.toFixed(4)}</span>
                  <span>{new Date(log.created_at).toLocaleTimeString("fr-FR")}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-[var(--text-secondary)] text-sm">
            Aucune activite pour le moment.
          </div>
        )}
      </div>
    </div>
  );
}
