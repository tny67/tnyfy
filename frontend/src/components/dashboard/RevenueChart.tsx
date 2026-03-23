"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const placeholderData = [
  { date: "Lun", revenue: 0 },
  { date: "Mar", revenue: 0 },
  { date: "Mer", revenue: 0 },
  { date: "Jeu", revenue: 0 },
  { date: "Ven", revenue: 0 },
  { date: "Sam", revenue: 0 },
  { date: "Dim", revenue: 0 },
];

export function RevenueChart() {
  return (
    <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-5">
      <h3 className="text-sm font-medium text-[var(--text-secondary)] mb-4">
        Revenu (7 derniers jours)
      </h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={placeholderData}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
            <XAxis dataKey="date" stroke="var(--text-secondary)" fontSize={12} />
            <YAxis stroke="var(--text-secondary)" fontSize={12} />
            <Tooltip
              contentStyle={{
                backgroundColor: "var(--bg-secondary)",
                border: "1px solid var(--border)",
                borderRadius: "8px",
                color: "var(--text-primary)",
              }}
            />
            <Line
              type="monotone"
              dataKey="revenue"
              stroke="var(--accent)"
              strokeWidth={2}
              dot={{ fill: "var(--accent)" }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
