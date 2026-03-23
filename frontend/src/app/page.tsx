"use client";

import { StatsCard } from "@/components/dashboard/StatsCard";
import { RevenueChart } from "@/components/dashboard/RevenueChart";
import { RecentOrders } from "@/components/dashboard/RecentOrders";
import { AgentActivityFeed } from "@/components/agents/AgentActivityFeed";
import { useApi } from "@/hooks/useApi";
import { useWebSocket } from "@/hooks/useWebSocket";
import type { AnalyticsOverview } from "@/types/store";

export default function DashboardPage() {
  const { data: analytics } = useApi<AnalyticsOverview>("/api/v1/analytics/overview", 30000);
  const { events, connected } = useWebSocket();

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <div className="flex items-center gap-2 text-xs">
          <div className={`w-2 h-2 rounded-full ${connected ? "bg-[var(--success)]" : "bg-[var(--danger)]"}`} />
          <span className="text-[var(--text-secondary)]">
            {connected ? "Connecte en temps reel" : "Hors ligne"}
          </span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="Revenu Total"
          value={`${(analytics?.total_revenue ?? 0).toFixed(2)} EUR`}
          change={analytics?.total_revenue ? "+12%" : ""}
          trend={analytics?.total_revenue ? "up" : "neutral"}
        />
        <StatsCard
          title="Commandes"
          value={String(analytics?.total_orders ?? 0)}
          change={analytics?.total_orders ? "+8%" : ""}
          trend={analytics?.total_orders ? "up" : "neutral"}
        />
        <StatsCard
          title="Boutiques Actives"
          value={String(analytics?.active_stores ?? 0)}
          change=""
          trend="neutral"
        />
        <StatsCard
          title="Cout IA Aujourd'hui"
          value={`${(analytics?.ai_cost_today ?? 0).toFixed(2)} $`}
          change=""
          trend="neutral"
        />
      </div>

      {/* Charts & Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <RevenueChart />
        </div>
        <div>
          <AgentActivityFeed liveEvents={events} />
        </div>
      </div>

      {/* Recent Orders */}
      <RecentOrders />
    </div>
  );
}
