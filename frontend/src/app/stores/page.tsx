"use client";

export default function StoresPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Boutiques</h1>
        <div className="text-xs text-[var(--text-secondary)] bg-[var(--bg-card)] border border-[var(--border)] px-3 py-1.5 rounded-lg">
          L&apos;IA cree les boutiques automatiquement
        </div>
      </div>

      <div className="text-center py-16 bg-[var(--bg-card)] border border-[var(--border)] rounded-xl">
        <div className="text-4xl mb-4">🏪</div>
        <p className="text-[var(--text-secondary)]">
          Aucune boutique pour le moment.
        </p>
        <p className="text-xs text-[var(--text-secondary)] mt-2">
          Configurez vos credentials Shopify Partner dans Settings pour que l&apos;IA commence a creer des boutiques.
        </p>
      </div>
    </div>
  );
}
