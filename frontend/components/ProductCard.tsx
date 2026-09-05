type Product = { id: number; name: string; category: string; description: string; price_paise: number; stock: number };

export function ProductCard({ product, onBuy }: { product: Product; onBuy: (id: number) => void }) {
  return <article className="group flex min-h-[245px] flex-col justify-between rounded-sm border border-ink/10 bg-white/70 p-5 shadow-sm transition hover:-translate-y-1 hover:border-clay hover:shadow-[6px_6px_0_rgba(179,92,62,0.12)]">
    <div><div className="flex items-center justify-between"><p className="text-xs uppercase tracking-[0.14em] text-clay">{product.category}</p><span className="text-xs text-ink/40">{product.stock} in stock</span></div><h3 className="mt-5 text-2xl">{product.name}</h3><p className="mt-2 text-sm leading-6 text-ink/60">{product.description}</p></div>
    <div className="mt-8 flex items-end justify-between"><p className="text-xl">₹{(product.price_paise / 100).toLocaleString("en-IN")}</p><button onClick={() => onBuy(product.id)} className="bg-ink px-4 py-2 text-sm text-paper transition group-hover:bg-clay">Create test order ↗</button></div>
  </article>;
}
