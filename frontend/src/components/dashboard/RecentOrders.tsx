export function RecentOrders() {
  return (
    <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-5">
      <h3 className="text-sm font-medium text-[var(--text-secondary)] mb-4">
        Commandes recentes
      </h3>
      <div className="text-center py-8 text-[var(--text-secondary)] text-sm">
        Aucune commande pour le moment.
        <br />
        <span className="text-xs">
          Les commandes apparaitront ici en temps reel une fois les boutiques actives.
        </span>
      </div>
    </div>
  );
}
