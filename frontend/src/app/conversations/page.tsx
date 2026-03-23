"use client";

export default function ConversationsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Service Client (SAV)</h1>
      <div className="text-center py-16 bg-[var(--bg-card)] border border-[var(--border)] rounded-xl">
        <div className="text-4xl mb-4">💬</div>
        <p className="text-[var(--text-secondary)]">
          Les conversations clients gerees par l&apos;IA apparaitront ici.
        </p>
        <p className="text-xs text-[var(--text-secondary)] mt-2">
          Vous pourrez escalader vers un humain si necessaire.
        </p>
      </div>
    </div>
  );
}
