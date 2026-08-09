# pmo_epc2 — Cahier des Charges Fonctionnel (Django 5.1 + Next.js 15 / Postgres / Tailwind)

Version 1.0 — 07/08/2026 — Cible Arena (preview live) / VPS

---

## 1. Vision

Même **Project Control** que pmo_epc1 (portefeuille/conteneurs, projets/phases, commandes, tâches WBS 1..n, GED multi-conteneurs, planning double, coûts/EVM, risques/HSE, KPI). Différence : **API-first + preview live Next.js** (hot reload Arena).

## 2. Stack fonctionnelle

Postgres (JSONB, CTE), Django 5.1 (ORM + Services + Admin), Next.js 15 (App Router, Tailwind, shadcn/ui, TanStack Query/Table, Recharts), guardian. Même rôles que pmo_epc1.

## 3. Modèles (identiques pmo_epc1, adaptés Postgres)

`Conteneur`, `Phase`, `Projet(+phases dérivées/M2M)`, `Commande`, `Tache(parent/niveau 1..n + TacheLien FS/SS/FF/SF + TacheDocument M2M)`, `Document/Revision`, `Cout/Risque/HSE`, `ProjetCurvePoint`, `ForecastRule`. Contraintes `CHECK 0..100`, `niveau>=1`.

## 4. GED & Planning

Identiques pmo_epc1 (cycle vs versioning selon `ClasseDocumentaire.avec_cycle`, MDR, transmittals, MDDM). `planning` (services Python) vs `planning_project` (Baseline/Version/Dependance/Ressource/Calendrier/CP).

## 5. API

`/api/v1/projects`, `/commands`, `/tasks?niveau_lte=5`, `/documents`, `/planning/gantt`, `/evm/scurve` — mêmes Services Django que vues, consommés par Next.js.

## 6. UI & Preview

Next.js pages : `/dashboard`, `/projects`, `/tasks`, `/planning`, `/planning-projet`, `/documents`, `/costs`, `/risks`, `/hse`, `/reporting`. Preview Arena : `https://{port}-{sandbox}.e2b.app` → `next dev -H 0.0.0.0` proxie `/api` vers Django `8000`. `django-cors`, `ALLOWED_HOSTS` preview.

## 7. KPI & Flux

Mêmes flux que pmo_epc1 (tâche+doc, document REJ/IFA/APP, baseline→S-curve). Voir overview §3.

## 8. Diagrammes

Idem `docs/REFONTE_PMO_EPC_OVERVIEW.md`.
