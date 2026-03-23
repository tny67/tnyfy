"use client";

export function Header() {
  return (
    <header className="h-14 bg-[var(--bg-secondary)] border-b border-[var(--border)] flex items-center justify-between px-6">
      <div className="flex items-center gap-4">
        <span className="text-sm text-[var(--text-secondary)]">
          Monitoring Dashboard
        </span>
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 text-xs">
          <div className="w-2 h-2 rounded-full bg-[var(--success)]" />
          <span className="text-[var(--text-secondary)]">7 agents actifs</span>
        </div>
        <div className="text-xs text-[var(--text-secondary)]">
          Budget IA: 0.00$ / 50.00$
        </div>
      </div>
    </header>
  );
}
