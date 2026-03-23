interface StatsCardProps {
  title: string;
  value: string;
  change: string;
  trend: "up" | "down" | "neutral";
}

export function StatsCard({ title, value, change, trend }: StatsCardProps) {
  const trendColor =
    trend === "up"
      ? "text-[var(--success)]"
      : trend === "down"
        ? "text-[var(--danger)]"
        : "text-[var(--text-secondary)]";

  return (
    <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-5">
      <p className="text-sm text-[var(--text-secondary)]">{title}</p>
      <p className="text-2xl font-bold mt-1">{value}</p>
      {change && (
        <p className={`text-xs mt-2 ${trendColor}`}>
          {trend === "up" ? "+" : ""}
          {change} vs dernier mois
        </p>
      )}
    </div>
  );
}
