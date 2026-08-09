# pmo_epc3 — Cahier des Charges Fonctionnel (Next.js 15 / TypeScript / Prisma / SQLite→Postgres / Tailwind — 100% preview Arena)

Version 1.0 — 07/08/2026 — Cible **visualisable ici** (preview live Arena) + Vercel/VPS

---

## 1. Vision

Même **Project Control** que pmo_epc1/2 (conteneurs, projets/phases, commandes, tâches WBS 1..n avec `parent/niveau` + peer `FS/SS/FF/SF`, GED multi-conteneurs avec cycle *ou* versioning seul, double planning, coûts/EVM/S-curves/forecast, risques/HSE, KPI/RACI). Différence : **stack 100% JS, zéro infra PHP/Python à installer**, tout tourne en `npm run dev` avec preview live `https://{port}-{sandbox}.e2b.app`.

## 2. Parité fonctionnelle

Identique pmo_epc1 (voir `docs/pmo_epc1/CAHIER_CHARGES_FONCTIONNEL.md`) : CRUD projets/commandes/tâches/documents, MDR par commande, `TacheDocument` M2M, `TacheLien`, `parent/niveau` (filtre `<=5` → planning projet), transmittals/MDDM, EVM (PV/EV/AC/SPI/CPI/EAC), S-curves, risques/HSE, dashboards.

## 3. Différences UX (preview-first)

- Kanban + Gantt (gantt-task-react) + Table (TanStack) synchronisés sur même `tasks` store
- Upload drag&drop documents avec génération auto `code_documentaire`
- WBS tree éditable (parent glisser-déposer → `niveau` recalculé côté client + API)
- S-curves Recharts en live (granularité DAY→YEAR)

## 4. Diagrammes

Voir `docs/REFONTE_PMO_EPC_OVERVIEW.md` §3 (use case, classes, états, séquence, activité, flux EVM) — valables pmo_epc3.

## 5. Flux clés (identiques)

Tâche → doc → Gantt ; Document REJ/IFA/APP ; Baseline → CP → S-curve → alerte SPI/CPI.
