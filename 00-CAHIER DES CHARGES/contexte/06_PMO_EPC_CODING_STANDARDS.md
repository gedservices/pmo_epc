# PMO EPC Platform

# Coding Standards

Version : 1.0

---

# Objectif

Ce document définit les conventions de développement de PMO EPC Platform.

Son objectif est de garantir :

- une architecture homogène
- un code lisible
- une maintenance facilitée
- une forte réutilisation des composants
- une compatibilité entre les développements réalisés par différents développeurs ou assistants IA

Ces règles s'appliquent à l'ensemble du projet.

---

# Technologies

Le projet repose sur les technologies suivantes :

Backend

- Python 3
- Django
- PostgreSQL

Frontend

- HTML5
- Bootstrap 5
- Bootstrap Icons
- JavaScript ES6

---

# Architecture

Le projet suit une architecture modulaire.

Chaque domaine métier est une application Django indépendante.

Exemple

```
apps/

accounts/

projects/

contracts/

tasks/

planning/

planning_project/

documents/

costs/

risks/

reporting/
```

Chaque application doit être autonome.

---

# Organisation d'une application

Chaque application suit la même structure.

```
app/

admin.py

apps.py

forms.py

models.py

services/

tables.py

filters.py

urls.py

views.py

tests.py

templates/

static/

migrations/
```

Les nouveaux modules doivent respecter cette organisation.

---

# Services

Toute logique métier est placée dans le dossier :

```
services/
```

Exemple

```
services/

dashboard.py

statistics.py

list.py

detail.py
```

Une vue Django ne doit jamais contenir de logique métier importante.

---

# Views

Les vues Django jouent uniquement un rôle de contrôleur.

Responsabilités :

- vérifier les permissions
- appeler les services
- construire le contexte
- afficher le template

Les calculs sont interdits dans les vues.

---

# Models

Les modèles représentent uniquement les objets métier.

Ils peuvent contenir :

- propriétés
- méthodes simples
- calculs directement liés à l'objet

Ils ne doivent pas contenir :

- logique d'affichage
- requêtes complexes inter-applications
- génération de tableaux de bord

---

# Forms

Les formulaires utilisent exclusivement les ModelForm lorsque cela est possible.

Les validations métier sont réalisées dans :

```
clean()

clean_<field>()
```

Aucune validation JavaScript ne remplace les validations Django.

---

# Templates

Les templates restent le plus simples possible.

Ils ne doivent jamais contenir :

- calculs complexes
- requêtes
- logique métier

Les templates servent uniquement à afficher les données.

---

# Composants

Tous les composants réutilisables sont centralisés.

```
templates/base/components/
```

Exemples

```
cards/

tables/

forms/

detail/

widgets/

progress/

plannings/
```

Avant de créer un nouveau composant, vérifier qu'il n'existe pas déjà.

---

# CSS

Le CSS spécifique est regroupé dans :

```
static/css/
```

Éviter les styles inline.

Les classes Bootstrap sont privilégiées.

---

# JavaScript

Le JavaScript est limité aux interactions utilisateur.

Les traitements métier restent côté serveur.

---

# URLs

Les URLs utilisent systématiquement un namespace.

Exemple

```
projects:list

projects:create

projects:detail

projects:update

projects:delete
```

---

# Templates

Convention de nommage :

```
dashboard.html

list.html

detail.html

form.html

delete.html
```

Les pages spécialisées utilisent des noms explicites.

Exemple

```
gantt.html

calendar.html

retards.html

charge.html
```

---

# Services spécialisés

Préférer plusieurs petits services plutôt qu'un fichier unique.

Exemple

```
services/

dashboard.py

statistics.py

project.py

contract.py

task.py

gantt.py
```

---

# Imports

Ordre recommandé :

Python

Django

Bibliothèques externes

Applications internes

Imports locaux

---

# Variables

Utiliser des noms explicites.

Préférer

```
projet

commande

responsable

progression
```

à

```
p

c

r

prog
```

---

# Constantes

Les constantes métier doivent être regroupées.

Exemple

```
STATUS_OPEN

STATUS_CLOSED

STATUS_DELAYED
```

Éviter les chaînes codées en dur.

---

# Référentiels

Toutes les valeurs métier doivent provenir des référentiels.

Interdit :

```
if discipline == "ELE"
```

Préférer :

```
discipline.code
```

---

# Requêtes

Toujours optimiser les requêtes.

Utiliser :

```
select_related()

prefetch_related()

annotate()

aggregate()
```

Éviter les requêtes répétitives dans les boucles.

---

# Calculs

Les calculs sont centralisés.

Exemple

```
PlanningService

CostService

DocumentService

RiskService
```

Jamais dans les templates.

---

# Journalisation

Les erreurs importantes doivent être journalisées.

Éviter les print().

Utiliser :

```
logging
```

---

# Gestion des erreurs

Toujours gérer :

DoesNotExist

ValidationError

PermissionDenied

404

500

---

# Tests

Chaque nouveau service doit pouvoir être testé indépendamment.

Les services sont conçus pour être facilement unitaires.

---

# Réutilisation

Toute duplication de code doit être évitée.

Avant d'écrire une fonction :

- vérifier si elle existe déjà
- vérifier si un composant existe
- vérifier si un service similaire existe

---

# Évolution

Le projet est conçu pour évoluer pendant plusieurs années.

Toute nouvelle fonctionnalité doit :

- respecter l'architecture existante
- enrichir les composants communs
- éviter la création de variantes inutiles

---

# Règles générales

Toujours privilégier :

✔ simplicité

✔ lisibilité

✔ modularité

✔ réutilisation

✔ cohérence

plutôt que :

✘ optimisation prématurée

✘ duplication

✘ logique dispersée

✘ code spécifique à une seule page

---

# Philosophie

Le code doit être suffisamment clair pour qu'un nouveau développeur — ou une IA — puisse comprendre rapidement son fonctionnement.

Une fonctionnalité développée aujourd'hui doit pouvoir être réutilisée dans d'autres modules sans modification majeure.

La maintenabilité prime toujours sur la complexité.