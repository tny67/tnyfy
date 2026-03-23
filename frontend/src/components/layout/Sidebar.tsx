"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/", label: "Dashboard", icon: "grid" },
  { href: "/stores", label: "Boutiques", icon: "store" },
  { href: "/products", label: "Produits", icon: "package" },
  { href: "/analytics", label: "Analytics", icon: "chart" },
  { href: "/agents", label: "Agents IA", icon: "cpu" },
  { href: "/conversations", label: "SAV", icon: "message" },
  { href: "/settings", label: "Settings", icon: "settings" },
];

const icons: Record<string, string> = {
  grid: "M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z",
  store: "M3 3h18l-2 8H5L3 3zm2 8v10h14V11H5zm4 3h6",
  package: "M16.5 9.4l-9-5.19M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z",
  chart: "M18 20V10M12 20V4M6 20v-6",
  cpu: "M9 3v2M15 3v2M9 19v2M15 19v2M3 9h2M3 15h2M19 9h2M19 15h2M6 6h12v12H6z",
  message: "M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z",
  settings: "M12 15a3 3 0 100-6 3 3 0 000 6z",
};

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-[var(--bg-secondary)] border-r border-[var(--border)] flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-[var(--border)]">
        <h1 className="text-2xl font-bold">
          <span className="text-[var(--accent)]">tnyfy</span>
        </h1>
        <p className="text-xs text-[var(--text-secondary)] mt-1">
          AI E-Commerce Automation
        </p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                isActive
                  ? "bg-[var(--accent)] text-white"
                  : "text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-card)]"
              }`}
            >
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d={icons[item.icon]} />
              </svg>
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* Status */}
      <div className="p-4 border-t border-[var(--border)]">
        <div className="flex items-center gap-2 text-xs text-[var(--text-secondary)]">
          <div className="w-2 h-2 rounded-full bg-[var(--success)] animate-pulse" />
          Systeme autonome actif
        </div>
      </div>
    </aside>
  );
}
