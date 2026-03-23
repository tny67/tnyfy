"use client";

import { AgentActivityFeed } from "@/components/agents/AgentActivityFeed";

export default function AgentsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Agents IA</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AgentActivityFeed />

        <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-5">
          <h3 className="text-sm font-medium text-[var(--text-secondary)] mb-4">
            Cout IA
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-[var(--text-secondary)]">Aujourd&apos;hui</span>
              <span>0.00 $</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-[var(--text-secondary)]">Ce mois</span>
              <span>0.00 $</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-[var(--text-secondary)]">Budget max/jour</span>
              <span>50.00 $</span>
            </div>
            <div className="w-full bg-[var(--bg-secondary)] rounded-full h-2 mt-2">
              <div
                className="bg-[var(--accent)] h-2 rounded-full"
                style={{ width: "0%" }}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-5">
        <h3 className="text-sm font-medium text-[var(--text-secondary)] mb-4">
          Historique des actions
        </h3>
        <div className="text-center py-8 text-[var(--text-secondary)] text-sm">
          Aucune activite pour le moment.
        </div>
      </div>
    </div>
  );
}
