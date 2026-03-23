"use client";

export default function ProductsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Produits</h1>
      <div className="text-center py-16 bg-[var(--bg-card)] border border-[var(--border)] rounded-xl">
        <div className="text-4xl mb-4">📦</div>
        <p className="text-[var(--text-secondary)]">
          L&apos;IA recherche les produits gagnants automatiquement.
        </p>
        <p className="text-xs text-[var(--text-secondary)] mt-2">
          Les produits trouves avec leur score apparaitront ici.
        </p>
      </div>
    </div>
  );
}
