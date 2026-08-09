# pmo_epc1 — Cahier des Charges Fonctionnel (PHP 8.2 / Laravel 12 / MySQL 8.4 / Bootstrap 5)

Version 1.0 — 07/08/2026 — Cible OVH mutualisé Pro

---

## 1. Vision

Plateforme **Project Control** pour portefeuilles EPC/EPCM : délais, coûts/EVM, GED multi-conteneurs, risques/HSE, KPI, reporting. Même périmètre que pmo_epc2, implémentation Laravel.

## 2. Acteurs & Rôles

ADMIN, PMO, MANAGER, LEAD_DOC_CONTROLLER, DOC_CONTROLLER, LEADER_TECHNIQUE, SPECIALIST, MEMBER, CONTRACTOR (+ guardia via Spatie Permission + Policies).

## 3. Conteneurs & Portefeuille

- CRUD Conteneur (ordre, actif, archive), migration `RUNNING→COM→ASBUILT` tracée (`migration_conteneur_logs`) : condition toutes `commandes=Terminée` + docs `Finalisé`, lecture seule hors RUNNING sauf ADMIN.
- Dashboard portefeuille : filtres par conteneur/entité/site/phase, KPIs consolidés.

## 4. Projets

- Code unique, type_projet, entités/sites M2M, pays/site/secteur, responsable, priorité/statut, dates prévues/réelles, budget prévu/réel, progression pondérée, EVM (PV/EV/AC, SPI/CPI), `est_generique/est_lecture_seule`, `phases` (dérivées commandes ou M2M).
- Actions : CRUD, scurve (`projet_curve_points` granularité DAY→YEAR), `forecast_rules` (CPI/SPI/HYBRID), migration conteneur.

## 5. Commandes

- `code_commande` unique, `code_originator` 4 chars (regex `^[A-Z0-9]{4}$` convention), `projet_id FK CASCADE`, `phase_id FK`, `entite_contractor_id FK`, `contractor` libellé, statut/priorité, pays/site/secteur, dates, budget, poids, `duree_revue_*`, EVM, `est_generique`.
- 1 commande = 1 phase + 1 fournisseur.

## 6. Tâches (Phase 1 validée)

- `projet_id FK required` + `commande_id FK nullable` (vérité EVM), `parent_id Self FK CASCADE`, `niveau` auto (`1` ou `parent.niveau+1`, filtre `<=5` planning projet), `phase_id`, `discipline_id`, `responsable_id`, `poids/avancement 0..100`, dates prévues/réelles, coûts, EVM, `est_en_retard/est_jalon`.
- `tache_liens` (peer `FS/SS/FF/SF` + `decalage_jours`) + `tache_documents` (M2M vers `documents`, `role`).
- `historique_taches` (champ/anc/nouv/modifie_par).
- WBS hiérarchique, Gantt opérationnel (tous niveaux), planning projet filtré 1..5.

## 7. GED central

- `documents` (code_documentaire unique, projet_id, commande_id nullable, discipline/phase/classe/type, statut_actuel, revision, originator) + `document_revisions` (fichier, statut, code_retour, commentaire, auteur, date_emission).
- Référentiels : `Pays/Site/Secteur/Systeme/SousSysteme`, `Phase`, `Discipline`, `ClasseDocumentaire(avec_cycle)`, `DocTypeTechnique`, `StatutCycleVie`, `SequenceStatut`, `Originator`.
- Règles : MDR = vue `documents WHERE commande_id=X`, séquence statuts = `Phase+Classe` si `avec_cycle`, sinon versioning seul. Numérotation auto `[PAYS]-[SITE]-[SECTEUR]-[ORIG]-[DISC]-[TYPE]-[SEQ]`.
- Transmittals + MDDM (revues Company/Contractor).

## 8. Planning

- **Opérationnel** (`planning/*`) : dashboard, Gantt, calendrier, retards, jalons, charge, `par_projet/commande/responsable` — services sur `taches`.
- **Moteur** (`planning-projet/*`) : baselines/versions/dépendances/ressources/calendriers/contraintes/chemin critique (Phase 2).

## 9. Coûts/EVM, Risques, HSE, Reporting

- Coûts : budget/engagé/réel, EAC/ETC/VAC, courbes S. Risques : matrice/heatmap. HSE : incidents/TRIR/LTIR. Reporting : dashboards + exports + Power BI.

## 10. KPI exhaustifs

Délais (SPI, retards, jalons), Coûts (CPI, EAC), Docs (IFR/IFA, délais revue, écarts prévu/réel), Risques, HSE.

## 11. Flux clés

- Création tâche → validation niveau → liaison docs → recalcul Gantt/charge.
- Document : MDR → upload → transmittal → revue → code_retour → nouvelle révision → Approuvé.
- Baseline : WBS → dépendances → CP → baseline → exec → S-curve → alerte SPI/CPI.

## 12. Diagrammes

Voir `docs/REFONTE_PMO_EPC_OVERVIEW.md` §3 (use case, classes, états, séquence, activité, flux EVM) — valables pmo_epc1.
