type Product = { id: number; name: string; category: string; description: string; price_paise: number; stock: number };

export function ProductCard({ product, onBuy }: { product: Product; onBuy: (id: number) => void }) {
  return <article className="flex flex-col justify-between border border-ink/15 bg-white/40 p-5">
    <div><p className="text-xs uppercase tracking-[0.14em] text-clay">{product.category}</p><h3 className="mt-3 text-2xl">{product.name}</h3><p className="mt-2 text-sm leading-6 text-ink/65">{product.description}</p></div>
    <div className="mt-8 flex items-end justify-between"><p className="text-xl">₹{(product.price_paise / 100).toLocaleString("en-IN")}</p><button onClick={() => onBuy(product.id)} className="bg-ink px-4 py-2 text-sm text-paper transition hover:bg-clay">Buy</button></div>
  </article>;
}
