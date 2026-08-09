# Refonte PMO EPC — Vue d'ensemble (V3 — 07/08/2026)

> Synthèse pour refondre l'actuel `pmo_epc` (Django/Postgres) en **deux cibles** :
> - **pmo_epc1** : PHP 8.2 / Laravel 12 / MySQL 8.4 / Bootstrap 5 — **déployable OVH mutualisé Pro**
> - **pmo_epc2** : Stack native Arena avec **prévisualisation live** — Django 5.1 + Next.js 15 + Tailwind + Postgres — **VPS/PaaS**

---

## 1. Pourquoi deux cibles ?

| Critère | pmo_epc1 (Laravel) | pmo_epc2 (Arena) |
|---|---|---|
| Hébergement | OVH mutualisé Pro (PHP only, pas de Python) → coût mini | VPS OVH / PaaS (Fly/Render) → Python OK, preview live |
| Prévisualisation | Blade/Livewire, preview simple | Next.js + API Django, hot reload + preview Arena intégrée |
| Équipe | PHP/Laravel largement connu chez GED | Python/Django déjà initié, plus riche pour EVM/IA |
| Base | MySQL 8.4 (mutualisé) | PostgreSQL (moteur EVM, JSONB, CTE WBS) |
| UI | Bootstrap 5 + Livewire 3 + Alpine | Tailwind + shadcn + React Query |

**Les deux partagent le même modèle métier (Phase 1 validée : `Tache.parent/niveau` + `TacheLien` + `TacheDocument`)** — seule l'implémentation change.

---

## 2. Périmètre fonctionnel commun (Project Control)

- Portefeuille par **Conteneur** (RUNNING/COM/ASBUILT/ARCHIVE administrable) + migration tracée
- **Projet** (phases dynamiques via `Phase`), **Commande** (1 phase + 1 fournisseur + originator 4 chars), **Tâche** WBS `1..n` (1..5 → planning projet, 6..n opérationnel seul) avec `parent` + `TacheLien` peer `FS/SS/FF/SF`
- **GED central** multi-conteneurs (cycle vie *ou* versioning seul) : `Document`/`Revision`, MDR par commande, `TacheDocument` M2M, transmittals, MDDM, revues
- **Planning** : opérationnel (Gantt/calendrier/retards/charge) vs moteur planning projet (baseline/version/dépendances/ressources/calendriers/chemin critique)
- **Coûts/EVM** : PV/EV/AC, SPI/CPI, EAC/ETC/VAC, S-curves + forecast gaussien, cash-flow
- **Risques/HSE** : matrice, heatmap, TRIR/LTIR
- **KPI + Reporting** : exhaustifs par module + RACI

Voir `docs/pmo_epc1/CAHIER_CHARGES_FONCTIONNEL.md` (détails) et Mermaid ci-dessous.

---

## 3. Mermaid — Référence unique (valable pmo_epc1 + pmo_epc2)

### 3.1 Use Cases

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

### 3.2 Classes (domaine)

```mermaid
classDiagram
  class Conteneur
  class Phase
  class Projet { code budget PV/EV/AC }
  class Commande { code_commande originator[4] phase fournisseur }
  class Tache { projet FK commande* parent niveau 1..n poids av. PV/EV/AC }
  class TacheLien { FS/SS/FF/SF lag }
  class TacheDocument
  class Document { code_doc classe type statut rev }
  class DocumentRevision { fichier code_retour }
  class Cout
  class Risque
  class HSE
  Conteneur "1" --> "N" Projet
  Projet "1" --> "N" Commande
  Phase "N" --> "N" Projet
  Phase "1" --> "N" Commande
  Projet "1" --> "N" Tache
  Commande "1" --> "N" Tache
  Tache "1" --> "0..1" Tache : parent
  Tache "N" --> "N" Tache : TacheLien
  Tache "N" --> "N" Document : TacheDocument
```

### 3.3 États Document

```mermaid
stateDiagram-v2
  [*] --> Prev : MDR créé
  Prev --> Emis : upload Contractor
  Emis --> EnRevue : transmittal
  EnRevue --> REJ : REJ
  EnRevue --> IFA : IFA/IFC
  EnRevue --> APP : APP/IFR
  REJ --> Emis : Rev B
  IFA --> Emis : Rev C
  APP --> [*]
  note right of EnRevue : séquence Phase+Classe\nou versioning seul (factures)
```

### 3.4 États Projet/Conteneur

```mermaid
stateDiagram-v2
  [*] --> Ouvert
  Ouvert --> EnCours : kickoff
  EnCours --> EnAttente
  EnAttente --> EnCours
  EnCours --> Suspendu
  Suspendu --> EnCours
  EnCours --> Cloture : toutes commandes Terminées + docs Finalisés
  Cloture --> RUNNING : conteneur RUNNING
  RUNNING --> COM : migration PMO
  COM --> ASBUILT : migration
  ASBUILT --> [*]
```

### 3.5 Activité Baseline

```mermaid
flowchart TD
  A[WBS 1..5] --> B[Dépendances FS/SS]
  B --> C[Chemin critique]
  C --> D[Baseline]
  D --> E{Exec}
  E --> F[PV/EV/AC]
  F --> G[S-curve+forecast]
  G --> H{SPI/CPI<1?}
  H -->|oui| I[Warning+replan]
  H -->|non| E
```

### 3.6 Séquence tâche+doc

```mermaid
sequenceDiagram
  participant U
  participant FE
  participant API
  participant DB
  U->>FE: créer tâche parent? niveau=parent+1
  FE->>API: POST /taches
  API->>DB: insert Tache
  U->>FE: lier doc existant
  FE->>API: POST /taches/{id}/documents
  API->>DB: TacheDocument
  API-->>U: Gantt recalculé
```

### 3.7 Flux EVM

```mermaid
flowchart LR
  P[Planned Value] --> SPI
  E[Earned Value] --> SPI & CPI & EAC
  A[Actual Cost] --> CPI
  SPI{SPI=E/P} --> Scurve
  CPI{CPI=E/A} --> EAC
  EAC --> Forecast
```

---

## 4. Cahiers livrés

- `docs/pmo_epc1/CAHIER_CHARGES_FONCTIONNEL.md` — fonctionnel exhaustif
- `docs/pmo_epc1/CAHIER_CHARGES_TECHNIQUE.md` — technique Laravel/MySQL
- `docs/pmo_epc2/CAHIER_CHARGES_FONCTIONNEL.md` — idem (même périmètre, adaptations preview)
- `docs/pmo_epc2/CAHIER_CHARGES_TECHNIQUE.md` — technique Django+Next/Postgres

Voir ces 4 fichiers pour le détail par module, flux, KPI, schémas.
