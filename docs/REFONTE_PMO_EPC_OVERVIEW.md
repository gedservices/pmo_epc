# Refonte PMO EPC — Vue d'ensemble (V3 — 07/08/2026)

> Actuel `pmo_epc` (Django/Postgres) → **3 cibles** :
> - **pmo_epc1** : PHP 8.2 / Laravel 12 / MySQL 8.4 / Bootstrap 5 — **OVH mutualisé Pro**
> - **pmo_epc2** : Django 5.1 + Next.js 15 + Tailwind + Postgres — **VPS/PaaS, preview Arena via proxy**
> - **pmo_epc3** : Next.js 15 / TypeScript / Prisma / SQLite→Postgres / Tailwind — **100% visualisable ici** (`npm run dev`)

---

## Stacks comparées

| Critère | pmo_epc1 (Laravel) | pmo_epc2 (Django+Next) | **pmo_epc3 (Next fullstack) ⭐ visualisable** |
|---|---|---|---|
| Hébergement | OVH mutualisé (PHP only) | VPS/PaaS | Vercel / VPS / **Arena preview** |
| Preview | Blade | Next proxie Django | **Direct `next dev -H 0.0.0.0`** |
| DB | MySQL 8.4 | Postgres | SQLite dev → Postgres prod |
| Lancement | `php artisan serve` | `django + next` 2 serveurs | `npm run dev` 1 serveur |

Modèle métier identique (Phase 1 : `Tache.parent/niveau` + `TacheLien` + `TacheDocument`).

---

## Mermaid — Référence unique (3 cibles)

### Use Cases

```mermaid
flowchart LR
  PMO[PMO/Admin] --> UC1[Portefeuille & Conteneurs]
  PMO --> UC2[Projets & Phases]
  PMO --> UC3[Commandes]
  PM --> UC4[Planning projet\nbaseline/CP]
  OPS --> UC5[Tâches opérationnel\nGantt/retards/charge]
  DC --> UC6[GED\nMDR/revisions]
  DC --> UC7[Transmittals & MDDM]
  DC --> UC8[Revues Company/Contractor]
  COST --> UC9[Coûts & EVM\nS-curve/forecast]
  RISK --> UC10[Risques & HSE]
  UC1 & UC2 & UC3 & UC4 & UC5 & UC6 & UC9 & UC10 --> UC11[Reporting & KPI]
```

### Classes

```mermaid
classDiagram
  class Conteneur
  class Phase
  class Projet { code phases budget PV/EV/AC }
  class Commande { code_commande originator[4] phase fournisseur }
  class Tache { projet FK commande* parent niveau poids av. }
  class TacheLien { FS/SS/FF/SF lag }
  class TacheDocument
  class Document { code_doc classe type statut }
  class DocumentRevision { fichier code_retour }
  class Cout
  class Risque
  Conteneur "1" --> "N" Projet
  Phase "N" --> "N" Projet
  Phase "1" --> "N" Commande
  Projet "1" --> "N" Commande
  Projet "1" --> "N" Tache
  Tache "1" --> "0..1" Tache : parent
  Tache "N" --> "N" Tache : TacheLien
  Tache "N" --> "N" Document : TacheDocument
```

### États Document

```mermaid
stateDiagram-v2
  [*] --> Prev : MDR créé
  Prev --> Emis : upload
  Emis --> EnRevue : transmittal
  EnRevue --> REJ : REJ
  EnRevue --> IFA : IFA/IFC
  EnRevue --> APP : APP/IFR
  REJ --> Emis : Rev B
  IFA --> Emis : Rev C
  APP --> [*]
```

### États Projet/Conteneur

```mermaid
stateDiagram-v2
  [*] --> Ouvert
  Ouvert --> EnCours
  EnCours --> Cloture : cmd Terminées + docs Finalisés
  Cloture --> RUNNING
  RUNNING --> COM : migration PMO
  COM --> ASBUILT
  ASBUILT --> [*]
```

### Activité Baseline

```mermaid
flowchart TD
  A[WBS 1..5] --> B[Dépendances]
  B --> C[Chemin critique]
  C --> D[Baseline]
  D --> E{Exec}
  E --> F[PV/EV/AC]
  F --> G[S-curve]
  G --> H{SPI/CPI<1?}
  H -->|oui| I[replan]
  H -->|non| E
```

### Séquence & Flux EVM

```mermaid
sequenceDiagram
  participant U
  participant FE
  participant API
  participant DB
  U->>FE: créer tâche (parent→niveau)
  FE->>API: POST /taches
  API->>DB: Tache
  U->>FE: lier doc
  FE->>API: POST /taches/{id}/documents
  API->>DB: TacheDocument
```

```mermaid
flowchart LR
  P[PV] --> SPI
  E[EV] --> SPI & CPI
  A[AC] --> CPI
  SPI --> Scurve
  CPI --> EAC --> Forecast
```

---

## Livrables

- `docs/pmo_epc1/*` — pmo_epc1
- `docs/pmo_epc2/*` — pmo_epc2
- `docs/pmo_epc3/*` — pmo_epc3 (preview)
- `pmo_epc3/` — squelette Next exécutable (`npm run dev`)
