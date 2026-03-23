"use client";

import { useState, useEffect } from "react";
import { useApi, apiPost } from "@/hooks/useApi";

interface SettingsData {
  shopify_partner_email: string;
  has_shopify_password: boolean;
  has_anthropic_key: boolean;
  daily_budget: number;
  max_stores: number;
  system_ready: boolean;
}

export default function SettingsPage() {
  const { data: savedSettings } = useApi<SettingsData>("/api/v1/settings");
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const [config, setConfig] = useState({
    shopify_partner_email: "",
    shopify_partner_password: "",
    anthropic_api_key: "",
    daily_budget: 50,
    max_stores: 5,
  });

  useEffect(() => {
    if (savedSettings) {
      setConfig((prev) => ({
        ...prev,
        shopify_partner_email: savedSettings.shopify_partner_email || "",
        daily_budget: savedSettings.daily_budget,
        max_stores: savedSettings.max_stores,
      }));
    }
  }, [savedSettings]);

  const handleChange = (field: string, value: string | number) => {
    setConfig((prev) => ({ ...prev, [field]: value }));
    setSaved(false);
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const body: Record<string, unknown> = {};
      if (config.shopify_partner_email) body.shopify_partner_email = config.shopify_partner_email;
      if (config.shopify_partner_password) body.shopify_partner_password = config.shopify_partner_password;
      if (config.anthropic_api_key) body.anthropic_api_key = config.anthropic_api_key;
      body.daily_budget = config.daily_budget;
      body.max_stores = config.max_stores;

      await apiPost("/api/v1/settings", body);
      setSaved(true);
    } catch (err) {
      alert("Erreur de sauvegarde: " + (err instanceof Error ? err.message : "inconnue"));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <h1 className="text-2xl font-bold">Configuration</h1>

      {savedSettings?.system_ready && (
        <div className="bg-[var(--success)]20 border border-[var(--success)] rounded-xl p-4 flex items-center gap-3">
          <div className="w-3 h-3 rounded-full bg-[var(--success)] animate-pulse" />
          <span className="text-sm" style={{ color: "var(--success)" }}>
            Systeme pret - Tnyfy est autonome
          </span>
        </div>
      )}

      <p className="text-sm text-[var(--text-secondary)]">
        Configurez vos credentials une seule fois. Tnyfy s&apos;occupe de tout ensuite.
      </p>

      {/* Shopify Partner */}
      <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-5 space-y-4">
        <div className="flex justify-between items-center">
          <h3 className="font-medium">Shopify Partner</h3>
          {savedSettings?.has_shopify_password && (
            <span className="text-xs text-[var(--success)]">Configure</span>
          )}
        </div>
        <div className="space-y-3">
          <div>
            <label className="text-xs text-[var(--text-secondary)] block mb-1">Email</label>
            <input
              type="email"
              value={config.shopify_partner_email}
              onChange={(e) => handleChange("shopify_partner_email", e.target.value)}
              className="w-full bg-[var(--bg-secondary)] border border-[var(--border)] rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[var(--accent)]"
              placeholder="votre@email.com"
            />
          </div>
          <div>
            <label className="text-xs text-[var(--text-secondary)] block mb-1">
              Mot de passe {savedSettings?.has_shopify_password && "(deja configure)"}
            </label>
            <input
              type="password"
              value={config.shopify_partner_password}
              onChange={(e) => handleChange("shopify_partner_password", e.target.value)}
              className="w-full bg-[var(--bg-secondary)] border border-[var(--border)] rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[var(--accent)]"
              placeholder={savedSettings?.has_shopify_password ? "••••••••" : "Entrez votre mot de passe"}
            />
          </div>
        </div>
      </div>

      {/* Claude API */}
      <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-5 space-y-4">
        <div className="flex justify-between items-center">
          <h3 className="font-medium">Claude API (Anthropic)</h3>
          {savedSettings?.has_anthropic_key && (
            <span className="text-xs text-[var(--success)]">Configure</span>
          )}
        </div>
        <div>
          <label className="text-xs text-[var(--text-secondary)] block mb-1">
            Cle API {savedSettings?.has_anthropic_key && "(deja configuree)"}
          </label>
          <input
            type="password"
            value={config.anthropic_api_key}
            onChange={(e) => handleChange("anthropic_api_key", e.target.value)}
            className="w-full bg-[var(--bg-secondary)] border border-[var(--border)] rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[var(--accent)]"
            placeholder={savedSettings?.has_anthropic_key ? "sk-ant-••••" : "sk-ant-..."}
          />
        </div>
      </div>

      {/* Budget */}
      <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-5 space-y-4">
        <h3 className="font-medium">Limites</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-xs text-[var(--text-secondary)] block mb-1">Budget IA max/jour ($)</label>
            <input
              type="number"
              value={config.daily_budget}
              onChange={(e) => handleChange("daily_budget", Number(e.target.value))}
              className="w-full bg-[var(--bg-secondary)] border border-[var(--border)] rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[var(--accent)]"
            />
          </div>
          <div>
            <label className="text-xs text-[var(--text-secondary)] block mb-1">Nombre max de boutiques</label>
            <input
              type="number"
              value={config.max_stores}
              onChange={(e) => handleChange("max_stores", Number(e.target.value))}
              className="w-full bg-[var(--bg-secondary)] border border-[var(--border)] rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[var(--accent)]"
            />
          </div>
        </div>
      </div>

      <button
        onClick={handleSave}
        disabled={saving}
        className="w-full bg-[var(--accent)] hover:bg-[var(--accent-light)] disabled:opacity-50 text-white py-2.5 rounded-lg text-sm font-medium transition-colors"
      >
        {saving ? "Sauvegarde en cours..." : saved ? "Sauvegarde ! Tnyfy est en marche" : "Sauvegarder et lancer Tnyfy"}
      </button>
    </div>
  );
}
