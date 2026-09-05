export function StatCard({ label, value }: { label: string; value: string }) {
  return <div className="border border-ink/10 bg-white/50 p-5"><p className="text-xs font-bold uppercase tracking-[0.16em] text-ink/45">{label}</p><p className="mt-3 text-3xl font-bold tracking-tight">{value}</p><div className="mt-4 h-1 w-10 bg-clay" /></div>;
}
