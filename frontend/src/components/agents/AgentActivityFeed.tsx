const agentTypes = [
  { name: "Orchestrator", status: "idle", color: "var(--accent)" },
  { name: "Niche Finder", status: "idle", color: "var(--warning)" },
  { name: "Store Creator", status: "idle", color: "var(--success)" },
  { name: "Product Research", status: "idle", color: "var(--accent-light)" },
  { name: "Listing Agent", status: "idle", color: "var(--success)" },
  { name: "Order Manager", status: "idle", color: "var(--warning)" },
  { name: "Customer Service", status: "idle", color: "var(--danger)" },
];

export function AgentActivityFeed() {
  return (
    <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-5">
      <h3 className="text-sm font-medium text-[var(--text-secondary)] mb-4">
        Agents IA
      </h3>
      <div className="space-y-3">
        {agentTypes.map((agent) => (
          <div
            key={agent.name}
            className="flex items-center justify-between text-sm"
          >
            <div className="flex items-center gap-2">
              <div
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: agent.color }}
              />
              <span>{agent.name}</span>
            </div>
            <span className="text-xs text-[var(--text-secondary)] bg-[var(--bg-secondary)] px-2 py-0.5 rounded">
              {agent.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
