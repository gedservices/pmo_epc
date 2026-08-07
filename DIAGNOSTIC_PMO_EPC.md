# Diagnostic PMO_EPC — Analyse initiale (07/08/2026)

> Dossier de travail : `C:\DevArea\MesProjets\Django_Projects\0611_gedservices_pmo`  
> Branche : `arena/019fda3f-pmo-epc` (commit `a472b35` - import initial)  
> Stack cible : **Python / Django 6.0.6 + PostgreSQL (port 5433) + django-guardian / crispy / tables2**

---

## 1. Vue d'ensemble — ce qui a été poussé

**4732 objets** poussés, 3.8 MiB. Structure :

```
backend/
  _old_apps/          # 10 apps legacy (squelettes vides) — à supprimer
  _old_core/          # ancien core/startproject — à supprimer
  apps/               # 13 apps actives
    accounts, contracts, core_ref, costs, dashboard, documents,
    planning, planning_project, projects, reporting, risks, tasks, workflows
  core/               # settings/urls/wsgi/asgi (propre)
  templates/          # ~40 templates (projects, tasks, planning...)
  static/
  manage.py
00-CAHIER DES CHARGES/ # 15 docs .md/.docx (archi, roadmap, spec, data-model)
script_db_model_creation.sql/.txt
.gitignore (minimal)
```

**Pas de** `requirements.txt` / `pyproject.toml` / `poetry.lock` / `.env.example` / `Dockerfile` / `README` technique dans `backend/`. C'est bloquant pour reproductibilité.

---

## 2. Ce qui est BON ✅

| Domaine | Constat |
|---------|---------|
| **Découpage métier** | 13 apps bien séparées, reflète le spec EPC : Projet -> Commande (Contract) -> Tâche -> Document -> Coûts/Risques/Planning |
| **Modèle Projets** | `Projet` riche : EVM (PV/EV/AC, SPI/CPI), budget, priorités, sites/entités M2M via tables de jonction, `ProjetCurvePoint` + `ForecastRule` (granularité DAY→YEAR, méthodes CPI/SPI/HYBRID), `MigrationConteneurLog` (traçabilité conteneur) |
| **Modèle Tâches** | Poids/avancement, jalons, EVM au niveau tâche, `est_en_retard` recalculé au `save()`, `HistoriqueTache` |
| **Documents EPC** | Cycle de vie complet : `Document` -> `DocumentRevision` + `ClasseDocumentaire/Discipline/StatutCycleVie/SequenceStatut/Originator` — conforme codification EPC |
| **Auth** | `User` custom `AbstractUser` avec `email` comme USERNAME_FIELD, rôles (ADMIN/PMO/LEAD_DOC_CONTROLLER/CONTRACTOR...), helpers `is_pmo`, `is_contractor_user`, support `guardian` pour permissions objet |
| **Core_ref** | Référentiels centralisés (Pays/Site/Secteur/Conteneur/Phase/Discipline) — bon pivot |
| **Settings** | `fr-fr` / `Africa/Libreville`, `humanize`, `crispy_bootstrap5`, `LOGIN_URL`, `PMO_CONFIG`, `MEDIA`, `WhiteNoise` déjà prévus |
| **Templates** | Base + partials déjà structurés (scurve, evm, planning, gantt) |

---

## 3. Dette & risques 🔴🟠

### 3.1 Critique (à traiter avant d'ajouter des features)

1. **Pas de gestion d'environnement** : `SECRET_KEY` hardcodé dans `core/settings.py`, `PASSWORD=openpgpwd`, `DEBUG=True` en dur. → **Fuite = compromission totale.** Passer à `python-decouple` / `django-environ` + `.env`.
2. **Pas de `requirements.txt`** : impossible de recréer l'env. Django 6.0.6 mentionné mais pas figé. `pip freeze` à faire immédiatement.
3. **Bases incohérentes** : `script_db_model_creation.sql` crée des tables `projets`, `taches`, `entites` en snake_case alors que Django crée `projects_projet`, `tasks_tache`, `accounts_entite` etc. Si le SQL a été exécuté à la main, double schéma en base.
4. **Doublons `planning` vs `planning_project`** : `planning_project` est vide (3 lignes) mais routé en double dans `core/urls.py` (`planning/` et `planning_projet/` pointent tous deux vers `apps.planning.urls`). Source de confusion + conflits de namespace.
5. **Dossiers legacy versionnés** : `_old_apps/` (10 apps vides) + `_old_core/` pèsent et polluent l'historique/search. À archiver hors Git ou supprimer.
6. **Duplication vues/forms** : `contracts/forms_old1.py`, `views_old1.py`, `views_old2.py`, `tasks/form_old1.html` etc. Dette de refactor non nettoyée.
7. **PostgreSQL port 5433** : non standard (5432). OK si volontaire mais à documenter ; sinon chaque dev/test va échouer.

### 3.2 Majeur

- **URL conflict** : `dashboard` monté 2 fois (`/dashboard/` et `/`) avec même namespace partiel → risque `NoReverseMatch`.
- **Migrations en pagaille** : `core_ref/migrations/_old_errors/` versionné, `core_ref` a 10 migrations dont certaines `Alter` qui se contredisent.
- **Pas de tests utiles** : tous les `tests.py` sont vides (`3` lignes par défaut). Aucune CI, pas de `pytest`/`coverage`.
- **Pas de contraintes métier en DB** : `Projet.code` unique OK, mais pas de `CheckConstraint` sur `avancement 0-100`, `poids >=0`, pas d'indexes sur `projet`, `commande`, `responsable`.
- **Logging incomplet** : `LOG_DIR` défini mais pas de `LOGGING` dict.
- **Static/Media** : `STATICFILES_STORAGE = whitenoise...` sans `whitenoise` dans requirements, va crasher en prod.
- **N+1 queries** : `recalculer_progression()` boucle Python sur toutes les tâches sans `select_related`/`aggregate`. À remplacer par `Sum(F(...))`.

### 3.3 Mineur / Hygiène

- `.gitignore` minimal (ne couvre pas `logs/`, `media/documents/`, `*.sqlite3`).
- `Nouveau Document texte.txt` vide + 3 fichiers `~$*.docx` (locks Word) versionnés.
- `00-CAHIER DES CHARGES` contient des doublons (`06_PMO...` vs `07...` guidelines).
- 13 apps mais `workflows`, `costs`, `reporting` sont squelettes (3 lignes chacun).
- `TIME_ZONE=Africa/Libreville` OK mais `USE_TZ=True` sans `ATOMIC_REQUESTS` — risque incohérences dates EPC.

---

## 4. Cartographie modèles (confirmée par code)

```
Entite (INTERNE/EXTERNE) ─┬─ User (email login, role, entite)
                          ├─ Projet ─┬─ Commande (par projet + originator 4 chars)
                          │          ├─ Tache (projet+commande, phase, discipline, poids, EVM)
                          │          ├─ Document (classe/type/discipline/phase, statut cycle de vie)
                          │          │    └─ DocumentRevision (fichier, code_retour)
                          │          ├─ ProjetCurvePoint (scurve par granularité)
                          │          └─ ForecastRule (OneToOne)
                          └─ ProjetEntite / ProjetSite (M2M)
Core_ref: Pays, Site, Secteur, Conteneur, Phase, Discipline, ClasseDocumentaire, DocTypeTechnique, StatutCycleVie, SequenceStatut, Originator
```

Manques vs spec `04. PMO_EPC_DATA_MODEL.md` : **Risque, Coût, Jalon** détaillés non implémentés (models vides).

---

## 5. Feuille de route proposée

### Phase 0 — Assainissement (1–2 jours) — **À FAIRE MAINTENANT**
- [ ] `pip freeze > backend/requirements.txt` + `requirements-dev.txt` ; figer `Django==6.0.6` etc.
- [ ] `.env.example` + `decouple` : `SECRET_KEY`, `DB_*`, `DEBUG`, `ALLOWED_HOSTS` hors code
- [ ] Nettoyage Git : `git rm -r backend/_old_apps backend/_old_core "00-CAHIER..." "~$*"` + `gitignore` complet
- [ ] Supprimer doublons `contracts/views_old*.py`, `documents/views_old1.py`, `tasks/form_old*.html`
- [ ] Clarifier `planning` vs `planning_project` (supprimer le vide ou fusionner)
- [ ] Corriger `core/urls.py` (un seul include planning, dashboard root sans namespace conflict)
- [ ] `README.md` technique (install, `python manage.py migrate`, `createsuperuser`, port 5433)

### Phase 1 — Fondations solides (1 semaine)
- [ ] Contraintes DB : `CheckConstraint avancement 0-100`, `Q(poids>=0)`, indexes sur `projet_id`, `responsable_id`, `statut`
- [ ] Refactor `Projet.recalculer_progression()` -> `aggregate(Sum(F('avancement')*F('poids')))`
- [ ] Signals : MAJ auto `ProjetCurvePoint` à chaque `Tache.save()` si `ForecastRule.mise_a_jour_auto`
- [ ] `LOGGING` dict + `guardian` permissions objet (PMO vs Contractor)
- [ ] Fixtures / `loaddata` pour référentiels (Pays, Sites, Phases) — remplacer SQL brut
- [ ] Tests unitaires modèles + `pytest` + CI GitHub Actions

### Phase 2 — EPC cœur (2–3 semaines)
- [ ] Implémenter `costs`, `risks`, `workflows` (modèles + vues) selon spec fonctionnelle
- [ ] Planning : Gantt, jalons, retards, charge — services déjà esquissés (`services/gantt.py`, `retards.py` etc.) à finaliser
- [ ] S-Curve / EVM dashboard : brancher `ProjetCurvePoint` + Chart.js (templates déjà présents)
- [ ] Documents : lifecycle complet + `django-guardian` + upload S3/local

### Phase 3 — Prod & hébergement
- [ ] **Hébergement** : Django ≠ OVH mutualisé Pro (PHP only). Choix : **VPS OVH** (tu gères) ou **PaaS** (Render/Fly/Pa en Europe) + Postgres managé. `.env` + `WhiteNoise` + `gunicorn`.
- [ ] Docker + `docker-compose` (web + db + nginx) pour dev/prod identiques
- [ ] Backup DB + `collectstatic` + `ALLOWED_HOSTS` prod

---

## 6. Prochaine étape — que veux-tu que je fasse en premier ?

**Je te propose de démarrer Phase 0 immédiatement dans cette branche `arena/019fda3f-pmo-epc`** :

1. Générer `requirements.txt` + `.env.example` + `settings` via `decouple`
2. Nettoyer `_old_*` et doublons + corriger `urls.py`
3. Pousser un commit `chore: assainissement Phase 0`

Tu confirmes que je lance **Phase 0** ? Ou tu préfères prioriser un module métier (ex: finaliser `planning` / `documents`) ?

> Dossier de travail reste bien `0611_gedservices_pmo` — tous les chemins ci-dessus sont absolus côté Windows, côté Arena c'est `/home/user/pmo_epc/backend/`.
