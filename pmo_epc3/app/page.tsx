export default function Home() {
  return (
    <main className="min-h-screen p-8 font-sans">
      <h1 className="text-3xl font-bold">pmo_epc3 — Preview Arena</h1>
      <p className="mt-2 text-zinc-600">Next.js 15 / Prisma / Tailwind — stack 100% visualisable ici. Même modèle métier que pmo_epc1/2.</p>
      <div className="mt-6 grid gap-4 md:grid-cols-3">
        {["Projets","Commandes","Tâches WBS 1..n"].map(k=> <div key={k} className="rounded-xl border p-4"><h2 className="font-semibold">{k}</h2><p className="text-sm text-zinc-500">CRUD + KPI + S-curve</p></div>)}
      </div>
      <div className="mt-6 rounded-xl border p-4">
        <h2 className="font-semibold">WBS parent/niveau</h2>
        <p className="text-sm">1..5 → planning_projet (baseline/CP), 6..n → opérationnel seul. Peer FS/SS/FF/SF + TacheDocument M2M.</p>
      </div>
      <p className="mt-6 text-sm">Prêt pour <code>prisma db push</code> puis CRUD. Voir docs/pmo_epc3/CAHIER_CHARGES_*.md</p>
    </main>
  );
}
