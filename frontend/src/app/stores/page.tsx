"use client";

import { useApi } from "@/hooks/useApi";
import type { Store } from "@/types/store";

const statusLabels: Record<string, { label: string; color: string }> = {
  creating: { label: "Creation en cours", color: "var(--warning)" },
  setup: { label: "Configuration", color: "var(--accent)" },
  active: { label: "Active", color: "var(--success)" },
  paused: { label: "En pause", color: "var(--text-secondary)" },
  error: { label: "Erreur", color: "var(--danger)" },
};

export default function StoresPage() {
  const { data: stores, loading } = useApi<Store[]>("/api/v1/stores", 15000);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Boutiques</h1>
        <div className="text-xs text-[var(--text-secondary)] bg-[var(--bg-card)] border border-[var(--border)] px-3 py-1.5 rounded-lg">
          L&apos;IA cree et gere les boutiques automatiquement
        </div>
      </div>

      {loading ? (
        <div className="text-center py-16 text-[var(--text-secondary)]">Chargement...</div>
      ) : stores && stores.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {stores.map((store) => {
            const status = statusLabels[store.status] || { label: store.status, color: "var(--text-secondary)" };
            return (
              <div
                key={store.id}
                className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-5 space-y-3"
              >
                <div className="flex justify-between items-start">
                  <h3 className="font-medium">{store.name}</h3>
                  <div className="flex items-center gap-1.5">
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: status.color }} />
                    <span className="text-xs" style={{ color: status.color }}>{status.label}</span>
                  </div>
                </div>
                {store.niche && (
                  <p className="text-xs text-[var(--text-secondary)]">Niche: {store.niche}</p>
                )}
                {store.shopify_domain && (
                  <p className="text-xs text-[var(--text-secondary)]">{store.shopify_domain}</p>
                )}
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--text-secondary)]">Revenu mensuel</span>
                  <span className="font-medium">{store.monthly_revenue.toFixed(2)} EUR</span>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="text-center py-16 bg-[var(--bg-card)] border border-[var(--border)] rounded-xl">
          <div className="text-4xl mb-4">🏪</div>
          <p className="text-[var(--text-secondary)]">
            Aucune boutique pour le moment.
          </p>
          <p className="text-xs text-[var(--text-secondary)] mt-2">
            Configurez vos credentials dans Settings pour que l&apos;IA commence.
          </p>
        </div>
      )}
    </div>
  );
}
