"use client";

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Analytics</h1>
      <div className="text-center py-16 bg-[var(--bg-card)] border border-[var(--border)] rounded-xl">
        <div className="text-4xl mb-4">📊</div>
        <p className="text-[var(--text-secondary)]">
          Les statistiques de ventes et conversions apparaitront ici.
        </p>
      </div>
    </div>
  );
}
