"use client";

import { useApi } from "@/hooks/useApi";
import type { Product } from "@/types/store";

export default function ProductsPage() {
  const { data: products, loading } = useApi<Product[]>("/api/v1/products", 15000);

  const getScoreColor = (score: number) => {
    if (score >= 80) return "var(--success)";
    if (score >= 60) return "var(--warning)";
    return "var(--danger)";
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Produits</h1>

      {loading ? (
        <div className="text-center py-16 text-[var(--text-secondary)]">Chargement...</div>
      ) : products && products.length > 0 ? (
        <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-[var(--border)] text-left text-[var(--text-secondary)]">
                <th className="px-4 py-3">Produit</th>
                <th className="px-4 py-3">Prix</th>
                <th className="px-4 py-3">Cout</th>
                <th className="px-4 py-3">Marge</th>
                <th className="px-4 py-3">Score</th>
                <th className="px-4 py-3">Statut</th>
              </tr>
            </thead>
            <tbody>
              {products.map((product) => {
                const margin = product.price > 0
                  ? (((product.price - product.cost_price) / product.price) * 100).toFixed(0)
                  : "0";
                return (
                  <tr key={product.id} className="border-b border-[var(--border)] hover:bg-[var(--bg-secondary)]">
                    <td className="px-4 py-3 font-medium max-w-[250px] truncate">{product.title}</td>
                    <td className="px-4 py-3">{product.price.toFixed(2)} EUR</td>
                    <td className="px-4 py-3 text-[var(--text-secondary)]">{product.cost_price.toFixed(2)} EUR</td>
                    <td className="px-4 py-3" style={{ color: Number(margin) > 50 ? "var(--success)" : "var(--warning)" }}>
                      {margin}%
                    </td>
                    <td className="px-4 py-3">
                      <span
                        className="inline-block px-2 py-0.5 rounded text-xs font-medium"
                        style={{ color: getScoreColor(product.research_score), backgroundColor: `${getScoreColor(product.research_score)}20` }}
                      >
                        {product.research_score.toFixed(0)}/100
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <span className="text-xs bg-[var(--bg-secondary)] px-2 py-0.5 rounded">
                        {product.status}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="text-center py-16 bg-[var(--bg-card)] border border-[var(--border)] rounded-xl">
          <div className="text-4xl mb-4">📦</div>
          <p className="text-[var(--text-secondary)]">
            L&apos;IA recherche les produits gagnants automatiquement.
          </p>
          <p className="text-xs text-[var(--text-secondary)] mt-2">
            Les produits trouves avec leur score apparaitront ici.
          </p>
        </div>
      )}
    </div>
  );
}
