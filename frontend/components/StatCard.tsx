export function StatCard({ label, value }: { label: string; value: string }) {
  return <div className="border-t border-ink/20 pt-3"><p className="text-xs uppercase tracking-[0.16em] text-clay">{label}</p><p className="mt-2 text-3xl">{value}</p></div>;
}
