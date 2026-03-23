"use client";

import { useState } from "react";

export default function SettingsPage() {
  const [config, setConfig] = useState({
    shopifyPartnerEmail: "",
    shopifyPartnerPassword: "",
    anthropicApiKey: "",
    dailyBudget: "50.00",
    maxStores: "5",
  });

  const handleChange = (field: string, value: string) => {
    setConfig((prev) => ({ ...prev, [field]: value }));
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <h1 className="text-2xl font-bold">Configuration</h1>
      <p className="text-sm text-[var(--text-secondary)]">
        Configurez vos credentials une seule fois. Tnyfy s&apos;occupe de tout ensuite.
      </p>

      {/* Shopify Partner */}
      <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-5 space-y-4">
        <h3 className="font-medium">Shopify Partner</h3>
        <div className="space-y-3">
          <div>
            <label className="text-xs text-[var(--text-secondary)] block mb-1">
              Email
            </label>
            <input
              type="email"
              value={config.shopifyPartnerEmail}
              onChange={(e) => handleChange("shopifyPartnerEmail", e.target.value)}
              className="w-full bg-[var(--bg-secondary)] border border-[var(--border)] rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[var(--accent)]"
              placeholder="votre@email.com"
            />
          </div>
          <div>
            <label className="text-xs text-[var(--text-secondary)] block mb-1">
              Mot de passe
            </label>
            <input
              type="password"
              value={config.shopifyPartnerPassword}
              onChange={(e) =>
                handleChange("shopifyPartnerPassword", e.target.value)
              }
              className="w-full bg-[var(--bg-secondary)] border border-[var(--border)] rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[var(--accent)]"
              placeholder="••••••••"
            />
          </div>
        </div>
      </div>

      {/* Claude API */}
      <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-5 space-y-4">
        <h3 className="font-medium">Claude API (Anthropic)</h3>
        <div>
          <label className="text-xs text-[var(--text-secondary)] block mb-1">
            Cle API
          </label>
          <input
            type="password"
            value={config.anthropicApiKey}
            onChange={(e) => handleChange("anthropicApiKey", e.target.value)}
            className="w-full bg-[var(--bg-secondary)] border border-[var(--border)] rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[var(--accent)]"
            placeholder="sk-ant-..."
          />
        </div>
      </div>

      {/* Budget */}
      <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-5 space-y-4">
        <h3 className="font-medium">Limites</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-xs text-[var(--text-secondary)] block mb-1">
              Budget IA max/jour ($)
            </label>
            <input
              type="number"
              value={config.dailyBudget}
              onChange={(e) => handleChange("dailyBudget", e.target.value)}
              className="w-full bg-[var(--bg-secondary)] border border-[var(--border)] rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[var(--accent)]"
            />
          </div>
          <div>
            <label className="text-xs text-[var(--text-secondary)] block mb-1">
              Nombre max de boutiques
            </label>
            <input
              type="number"
              value={config.maxStores}
              onChange={(e) => handleChange("maxStores", e.target.value)}
              className="w-full bg-[var(--bg-secondary)] border border-[var(--border)] rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[var(--accent)]"
            />
          </div>
        </div>
      </div>

      <button className="w-full bg-[var(--accent)] hover:bg-[var(--accent-light)] text-white py-2.5 rounded-lg text-sm font-medium transition-colors">
        Sauvegarder et lancer Tnyfy
      </button>
    </div>
  );
}
