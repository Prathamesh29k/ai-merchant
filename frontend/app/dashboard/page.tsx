"use client";

import { useEffect, useState } from "react";
import { ProductCard } from "../../components/ProductCard";
import { StatCard } from "../../components/StatCard";

const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

type Product = {
  id: number;
  name: string;
  category: string;
  description: string;
  price_paise: number;
  stock: number;
};

type Audit = {
  id: number;
  action: string;
  amount_paise: number;
  decision: string;
  explanation: string;
  agent_id: string;
};

function formatRupees(paise: number) {
  return `₹${(paise / 100).toLocaleString("en-IN")}`;
}

export default function DashboardPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [logs, setLogs] = useState<Audit[]>([]);
  const [revenue, setRevenue] = useState(0);
  const [query, setQuery] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);

  const refresh = () => {
    setLoading(true);
    Promise.all([
      fetch(`${API}/api/products`).then((response) => response.json()),
      fetch(`${API}/api/audit`).then((response) => response.json()),
      fetch(`${API}/api/audit/metrics`).then((response) => response.json()),
    ])
      .then(([catalog, audit, metrics]) => {
        setProducts(catalog);
        setLogs(audit);
        setRevenue(metrics.revenue_paise);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    refresh();
  }, []);

  const createOrder = (productId: number) => {
    fetch(`${API}/api/orders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ product_id: productId, quantity: 1, agent_id: "dashboard-demo" }),
    }).then(async (response) => {
      const data = await response.json();
      setMessage(response.ok ? `Order ${data.razorpay_order_id} created in Test Mode.` : data.detail?.message || "Order rejected by policy.");
      refresh();
    });
  };

  const visibleProducts = products.filter((product) => `${product.name} ${product.category}`.toLowerCase().includes(query.toLowerCase()));
  const approved = logs.filter((log) => log.decision === "approved").length;
  const rejected = logs.filter((log) => log.decision === "rejected").length;
  const approvalRate = logs.length ? Math.round((approved / logs.length) * 100) : 0;

  return (
    <main className="min-h-screen bg-[#f4f0e9] text-ink lg:pl-64">
      <aside className="fixed left-0 top-0 hidden h-screen w-64 border-r border-ink/10 bg-[#ebe6de] px-6 py-7 lg:block">
        <a href="/" className="flex items-center gap-3 text-lg font-bold"><span className="grid h-9 w-9 place-items-center bg-ink text-xs text-paper">A</span> AM/OS</a>
        <p className="mt-2 text-xs text-ink/45">Agent commerce infrastructure</p>
        <nav className="mt-12 space-y-1 text-sm">
          <p className="mb-3 px-3 text-[10px] font-bold uppercase tracking-[0.18em] text-ink/40">Workspace</p>
          <a href="/dashboard" className="flex items-center gap-3 bg-ink px-3 py-3 font-bold text-paper">▦ <span>Overview</span></a>
          <a href="#catalog" className="flex items-center gap-3 px-3 py-3 text-ink/60 hover:bg-white/60">⌘ <span>Catalog</span></a>
          <a href="#audit" className="flex items-center gap-3 px-3 py-3 text-ink/60 hover:bg-white/60">◷ <span>Audit trail</span></a>
          <a href="/checkout" className="flex items-center gap-3 px-3 py-3 text-ink/60 hover:bg-white/60">↗ <span>Buyer preview</span></a>
        </nav>
        <div className="absolute bottom-7 left-6 right-6 border-t border-ink/10 pt-5"><p className="text-[10px] font-bold uppercase tracking-[0.16em] text-ink/40">Environment</p><div className="mt-3 flex items-center gap-2 text-xs"><span className="h-2 w-2 rounded-full bg-green-600" /> Test Mode active</div><p className="mt-2 text-xs text-ink/45">Policy limit · ₹50 / agent / day</p></div>
      </aside>

      <div className="mx-auto max-w-[1440px] px-6 py-6 md:px-10">
        <header className="flex flex-wrap items-center justify-between gap-4 border-b border-ink/10 pb-5"><div className="flex items-center gap-3 lg:hidden"><span className="grid h-8 w-8 place-items-center bg-ink text-xs text-paper">A</span><strong>AM/OS</strong></div><div className="text-xs text-ink/45">Workspace / Overview</div><div className="flex items-center gap-4 text-xs"><span className="flex items-center gap-2"><span className="h-2 w-2 rounded-full bg-green-600" /> API operational</span><a href="/checkout" className="font-bold text-clay">Buyer preview →</a></div></header>

        <section className="flex flex-wrap items-end justify-between gap-6 py-10"><div><p className="text-xs font-bold uppercase tracking-[0.2em] text-clay">Merchant command centre</p><h1 className="mt-3 text-4xl font-bold tracking-tight md:text-5xl">Good morning, team.</h1><p className="mt-3 max-w-xl text-sm leading-6 text-ink/60">Your agent commerce layer is live. Review inventory, monitor decisions, and keep every payment action accountable.</p></div><div className="border border-ink/10 bg-white/50 px-5 py-4 text-right"><p className="text-[10px] font-bold uppercase tracking-[0.16em] text-ink/45">Today&apos;s policy posture</p><p className="mt-2 text-lg font-bold text-green-700">Healthy · Protected</p><p className="mt-1 text-xs text-ink/50">Daily limit enforced before payment</p></div></section>

        {message && <div className="mb-6 flex items-center justify-between border-l-4 border-clay bg-white/70 px-5 py-4 text-sm"><span>{message}</span><button onClick={() => setMessage("")} className="text-ink/40">Dismiss</button></div>}

        <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4"><StatCard label="Catalog items" value={String(products.length)} /><StatCard label="Paid revenue" value={formatRupees(revenue)} /><StatCard label="Approval rate" value={`${approvalRate}%`} /><StatCard label="Rejected by policy" value={String(rejected)} /></section>

        <section className="mt-10 grid gap-4 lg:grid-cols-[1fr_320px]"><div className="border border-ink/10 bg-white/50 p-5"><div className="flex flex-wrap items-end justify-between gap-4"><div><p className="text-[10px] font-bold uppercase tracking-[0.18em] text-clay">Inventory intelligence</p><h2 className="mt-2 text-2xl font-bold">Agent-readable catalog</h2></div><input value={query} onChange={(event) => setQuery(event.target.value)} className="w-full border border-ink/15 bg-[#f4f0e9] px-3 py-2 text-sm outline-none focus:border-clay sm:w-56" placeholder="Search catalog" /></div>{loading ? <p className="mt-8 text-sm text-ink/50">Loading catalog...</p> : <div id="catalog" className="mt-6 grid gap-4 md:grid-cols-2">{visibleProducts.map((product) => <ProductCard key={product.id} product={product} onBuy={createOrder} />)}</div>}</div><aside className="border border-ink/10 bg-ink p-6 text-paper"><p className="text-[10px] font-bold uppercase tracking-[0.18em] text-paper/45">Policy monitor</p><h2 className="mt-3 text-2xl font-bold">₹50 limit</h2><p className="mt-2 text-sm leading-6 text-paper/60">Every agent purchase is checked before a Razorpay order is created.</p><div className="mt-8 border-t border-paper/15 pt-5"><div className="flex justify-between text-xs"><span className="text-paper/50">Approved actions</span><strong>{approved}</strong></div><div className="mt-4 flex justify-between text-xs"><span className="text-paper/50">Blocked actions</span><strong className="text-orange-300">{rejected}</strong></div><div className="mt-5 h-1.5 bg-paper/15"><div className="h-full bg-clay" style={{ width: `${Math.max(approvalRate, 4)}%` }} /></div></div></aside></section>

        <section id="audit" className="mt-10 border border-ink/10 bg-white/50"><div className="flex flex-wrap items-end justify-between gap-4 border-b border-ink/10 px-5 py-5"><div><p className="text-[10px] font-bold uppercase tracking-[0.18em] text-clay">Observability</p><h2 className="mt-2 text-2xl font-bold">Decision log</h2></div><div className="text-right text-xs text-ink/45"><p>Immutable money-action trail</p><p className="mt-1">Showing latest {Math.min(logs.length, 100)} events</p></div></div><div className="overflow-x-auto"><table className="w-full min-w-[760px] text-left text-sm"><thead className="bg-[#ebe6de] text-[10px] font-bold uppercase tracking-[0.14em] text-ink/50"><tr><th className="px-5 py-3">Agent</th><th className="px-5 py-3">Action</th><th className="px-5 py-3">Amount</th><th className="px-5 py-3">Decision</th><th className="px-5 py-3">Reason</th></tr></thead><tbody>{logs.length === 0 ? <tr><td colSpan={5} className="p-10 text-center text-ink/45">No money actions yet. Create a test order above.</td></tr> : logs.map((log) => <tr key={log.id} className="border-t border-ink/10 hover:bg-[#f8f5ef]"><td className="px-5 py-4 font-mono text-xs">{log.agent_id}</td><td className="px-5 py-4 font-medium">{log.action}</td><td className="px-5 py-4 font-medium">{formatRupees(log.amount_paise)}</td><td className="px-5 py-4"><span className={`inline-flex px-2 py-1 text-[10px] font-bold uppercase tracking-wider ${log.decision === "approved" ? "bg-green-100 text-green-800" : "bg-orange-100 text-orange-800"}`}>{log.decision}</span></td><td className="max-w-lg px-5 py-4 text-xs leading-5 text-ink/60">{log.explanation}</td></tr>)}</tbody></table></div></section>
        <footer className="flex flex-wrap justify-between gap-3 py-8 text-xs text-ink/40"><span>AM/OS · Agent-ready commerce infrastructure</span><span>Razorpay Test Mode · Groq-ready · Audit protected</span></footer>
      </div>
    </main>
  );
}
