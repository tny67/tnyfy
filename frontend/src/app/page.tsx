"use client";

import { StatsCard } from "@/components/dashboard/StatsCard";
import { RevenueChart } from "@/components/dashboard/RevenueChart";
import { RecentOrders } from "@/components/dashboard/RecentOrders";
import { AgentActivityFeed } from "@/components/agents/AgentActivityFeed";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="Revenu Total"
          value="0 EUR"
          change="+0%"
          trend="up"
        />
        <StatsCard
          title="Commandes"
          value="0"
          change="+0%"
          trend="up"
        />
        <StatsCard
          title="Boutiques Actives"
          value="0"
          change=""
          trend="neutral"
        />
        <StatsCard
          title="Agents IA Actifs"
          value="0"
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
          <AgentActivityFeed />
        </div>
      </div>

      {/* Recent Orders */}
      <RecentOrders />
    </div>
  );
}
