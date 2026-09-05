export default function HomePage() {
  return (
    <main className="mx-auto max-w-6xl px-6 py-8 md:px-10 md:py-10">
      <nav className="flex items-center justify-between border-b border-ink/10 pb-5 text-sm">
        <a href="/" className="font-bold tracking-tight">AM/OS <span className="ml-2 font-normal text-ink/45">merchant control plane</span></a>
        <div className="flex items-center gap-6"><a href="/checkout" className="text-ink/60 hover:text-ink">Buyer view</a><a href="/dashboard" className="bg-ink px-4 py-2 text-paper transition hover:bg-clay">Dashboard</a></div>
      </nav>
      <section className="grid min-h-[72vh] items-center gap-16 py-20 md:grid-cols-[1.15fr_0.85fr]">
        <div>
          <div className="flex items-center gap-3 text-xs uppercase tracking-[0.2em] text-clay"><span className="h-2 w-2 rounded-full bg-clay" /> Live demo environment</div>
          <h1 className="mt-7 max-w-4xl text-6xl leading-[0.9] tracking-tight md:text-8xl">Commerce that can think with you.</h1>
          <p className="mt-8 max-w-xl text-xl leading-8 text-ink/65">A merchant operating system for AI buyers: discover products, explain recommendations, control spend, and leave an audit trail.</p>
          <div className="mt-10 flex flex-wrap gap-3"><a href="/checkout" className="bg-clay px-6 py-3 text-paper transition hover:bg-ink">Start as AI buyer</a><a href="/dashboard" className="border border-ink/20 px-6 py-3 transition hover:border-clay hover:text-clay">View merchant OS</a></div>
        </div>
        <div className="relative overflow-hidden border border-ink/15 bg-white/45 p-7 shadow-[12px_12px_0_rgba(32,37,34,0.08)]">
          <div className="absolute right-0 top-0 h-28 w-28 rounded-bl-full bg-clay/10" />
          <p className="relative text-xs uppercase tracking-[0.16em] text-ink/45">Policy snapshot</p>
          <p className="relative mt-8 text-7xl text-clay">₹50</p><p className="relative mt-1 text-lg">daily agent spending limit</p>
          <div className="relative mt-12 space-y-5 border-t border-ink/10 pt-5 text-sm"><p className="flex justify-between"><span className="text-ink/55">Payment layer</span><strong>Razorpay Test Mode</strong></p><p className="flex justify-between"><span className="text-ink/55">Decision layer</span><strong>FastAPI + SQLite</strong></p><p className="flex justify-between"><span className="text-ink/55">Intent layer</span><strong>Groq / local fallback</strong></p></div>
        </div>
      </section>
      <section className="grid gap-4 border-t border-ink/15 py-8 md:grid-cols-3"><div><p className="text-3xl text-clay">01</p><h2 className="mt-4 text-xl">Readable catalog</h2><p className="mt-2 text-sm leading-6 text-ink/60">Structured product context agents can query without guessing.</p></div><div><p className="text-3xl text-clay">02</p><h2 className="mt-4 text-xl">Guarded checkout</h2><p className="mt-2 text-sm leading-6 text-ink/60">Rules run before a payment order reaches Razorpay.</p></div><div><p className="text-3xl text-clay">03</p><h2 className="mt-4 text-xl">Accountable growth</h2><p className="mt-2 text-sm leading-6 text-ink/60">Upsells and money actions are visible in one audit trail.</p></div></section>
    </main>
  );
}
