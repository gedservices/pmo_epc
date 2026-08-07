# Architecture GED / Planning — Décisions Phase 0

> Complète `01. PMO_EPC_GUIDE_ARCHIECTURE_IA.md` et les 3 `.docx` de philosophie.
> À lire comme référence pour tout développement futur.

## 1. GED = Document lifecycle, pas seulement stockage

Le module `apps.documents` gère le **cycle de vie documentaire complet**, pas un simple drive :

- `Document` (code_documentaire unique, titre, projet/commande, discipline/phase/classe/type, statut cycle de vie, revision_actuelle, originator)
- `DocumentRevision` (fichier, statut, code_retour, commentaire, auteur, date_emission)
- Référentiels associés : `ClasseDocumentaire`, `DocTypeTechnique`, `StatutCycleVie`, `SequenceStatut`, `Originator`, `Discipline`, `Phase`

**Règle de modularité** : Les autres modules **n'embarquent jamais** de document binaire. Ils **référencent** un `Document` existant via FK/M2M. 
Exemple en cours : `Tache` pourra être liée à `0..N Documents` existants (via table de liaison à créer `TacheDocument`), sans dupliquer le fichier. Même principe pour `Commande` et `Projet`.

```
Projet ─┬─ Commande ─┬─ Tache ──○ Document (M2M via TacheDocument)
        │            └─ MDR (= vue filtrée des Documents de la Commande)
        └─ Documents (tous documents du projet, qu'ils soient liés à une tâche ou non)
```

Conséquence : le GED reste **source unique de vérité** ; planning/costs/risks ne font que **pointer**.

## 2. Deux plannings, deux responsabilités

### 2a. `apps.planning` — Suivi opérationnel (existant, à finaliser)
- **Sans modèle propre.** Vue analytique sur `Tache` (prévue vs réelle, avancement, poids, EVM).
- Services déjà présents : `dashboard`, `gantt`, `calendrier`, `charge`, `jalons`, `retards`, `par_projet`, `par_commande`, `par_responsable`.
- Abstraction : affiche l'évolution des tâches **ouvertes vs réelles**, qu'elles soient ou non liées à un planning projet, qu'elles aient un parent ou non.
- **Hiérarchie des tâches** : chaque `Tache` peut avoir `parent`/`enfants` ou `liées de même niveau` (dépendances). À modéliser via `TacheParent` (self-FK) + `TacheLien` (M2M symétrique avec type `FS/SS/FF/SF`). Niveaux 1..5 remontent dans la vue planning ; 6..n restent opérationnelles mais masquées du planning consolidé (filtrage par `niveau` / `profondeur`).

### 2b. `apps.planning_project` — Moteur planning projet (squelette, à construire)
- **Avec modèles propres** : `PlanningBaseline`, `PlanningVersion`, `PlanningRessource`, `PlanningCalendrier`, `PlanningContrainte`, `TacheDependance` (FS/SS...), `CheminCritique`.
- Fonctionne **comme MS Project / Primavera** : baselines, versions, nivellement, chemin critique, export.
- Se **synchronise** avec `Tache` (niveau 1-5) mais ne le remplace pas. Idée : `planning_project` génère / met à jour des `Tache` de niveau ≤5 ; le suivi opérationnel (`planning`) les affiche.

```
Tâche (niveau 1-5)  ←→  Planning Project (baseline, dépendances, ressources)
       ↕ (filtré)
Tâche (niveau 6-n)  →  masquée du planning, visible uniquement en suivi opérationnel
```

## 3. Règles d'implémentation à respecter

1. **Services > Vues** : toute logique métier dans `apps/planning/services/*.py` ou `apps/documents/services.py`, jamais dans `views.py`.
2. **Composants réutilisables** : `templates/plannings/*` mutualisés entre les deux plannings.
3. **Pas d'orphan** : toute tâche/document doit appartenir au `Projet générique` + `Commande générique` si aucun projet réel (règle GED spec V1).
4. **Conteneur = cycle de vie** : migration `RUNNING → COM → ASBUILT` tracée (`MigrationConteneurLog`), projet en conteneur non-RUNNING = lecture seule sauf ADMIN.
5. **Niveau de tâche** : ajouter `niveau` (int) + `parent` (self FK) à `Tache` avant de brancher le filtrage planning.

## 4. Vérification vs intention code actuel

- ✅ `planning` sans modèle, services bien découpés — conforme intention doc.
- ✅ `documents` avec cycle de vie et originator — conforme.
- ❌ `Tache` sans `parent`/`niveau`/`liens` — à ajouter pour gérer hiérarchie 1..n.
- ❌ `planning_project/models.py` vide (3 lignes) — attendu, mais doit rester vide jusqu'à Phase 2 (pas de CRUD task déguisé).
- ⚠️ `core/urls.py` dupliquait `apps.planning.urls` sous deux namespaces — **corrigé Phase 0** (`planning/` vs `planning-projet/`).
