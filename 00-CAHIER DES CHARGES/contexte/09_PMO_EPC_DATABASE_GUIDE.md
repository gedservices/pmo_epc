# PMO EPC Platform

# Database Guide

Version : 1.0

---

# Objectif

Ce document décrit l'architecture de la base de données de PMO EPC Platform.

Il constitue la référence officielle concernant :

- la modélisation des données
- les conventions de nommage
- les relations entre les modules
- les règles de conception
- les performances
- les migrations

La base de données est le socle fonctionnel de toute la plateforme.

---

# Technologie

SGBD officiel

PostgreSQL

ORM

Django ORM

Toutes les évolutions doivent rester compatibles avec Django.

---

# Philosophie

La base est organisée selon les domaines métier.

Chaque application Django possède ses propres tables.

Les relations sont réalisées par clés étrangères.

Les duplications de données sont interdites.

---

# Architecture générale

```
Utilisateurs

↓

Portefeuille

↓

Projets

↓

Commandes

↓

Tâches

↓

Planning

↓

GED

↓

Pilotage

↓

Reporting
```

Les modules sont indépendants mais fortement liés.

---

# Organisation des applications

```
accounts

core_ref

projects

contracts

tasks

planning

planning_project

documents

costs

risks

reporting
```

Chaque application possède ses propres modèles.

---

# Référentiels

Le module :

```
core_ref
```

contient les données de référence.

Exemples

Pays

Entités

Sites

Disciplines

Phases

Statuts

Priorités

Types documentaires

Ces données sont utilisées par l'ensemble de la plateforme.

---

# Clés primaires

Toutes les tables utilisent :

```
id
```

AutoField ou BigAutoField.

Les codes métier ne remplacent jamais les clés techniques.

---

# Codes métier

Les objets métier possèdent un code unique.

Exemples

```
PJ-0001

CTR-0015

TSK-00248

DOC-12584
```

Ces codes sont visibles par les utilisateurs.

---

# Relations

Toujours utiliser :

ForeignKey

OneToOne

ManyToMany

Éviter les champs texte contenant des identifiants.

---

# Suppression

Les suppressions physiques doivent rester exceptionnelles.

Préférer :

```
actif

archive

supprime_logiquement
```

lorsque cela est pertinent.

---

# Historisation

Les objets critiques doivent conserver un historique.

Exemples

Projet

Commande

Document

Planning

Transmittal

Workflow

---

# Dates

Convention.

```
date_creation

date_modification

date_debut_prevue

date_fin_prevue

date_debut_reelle

date_fin_reelle
```

Ne jamais utiliser plusieurs conventions différentes.

---

# Utilisateurs

Convention.

```
cree_par

modifie_par

responsable

valide_par
```

---

# Décimaux

Utiliser :

DecimalField

pour :

Budgets

Coûts

Montants

Valeurs EVM

Ne jamais utiliser FloatField pour les montants financiers.

---

# Pourcentages

Toujours stockés entre :

0

et

100

Exemple

```
avancement = 72.5
```

---

# États

Les états doivent être contrôlés.

Utiliser :

Choices

ou

Tables de référence

Jamais des chaînes libres.

---

# Performances

Toujours indexer :

ForeignKey

Codes

Dates fréquemment recherchées

Statuts

---

# Optimisation ORM

Toujours privilégier :

```
select_related()

prefetch_related()

annotate()

aggregate()

only()

defer()
```

Éviter les requêtes N+1.

---

# Contraintes

Utiliser les contraintes PostgreSQL lorsque possible.

Exemples

UniqueConstraint

CheckConstraint

Indexes

---

# Transactions

Les opérations critiques doivent être atomiques.

Utiliser :

```
transaction.atomic()
```

pour :

création complexe

import

suppression multiple

workflow

---

# Migrations

Une migration doit :

être courte

être explicite

être testée

Une migration ne doit jamais contenir de logique métier.

---

# Nommage

Tables

nom_application_nomobjet

Exemple

```
projects_projet

contracts_commande

tasks_tache
```

Colonnes

snake_case

---

# Relations entre modules

## Projects

Projet

↓

Commandes

↓

Tâches

↓

Documents

↓

Planning

↓

Coûts

↓

Risques

↓

Reporting

Le projet est l'objet central.

---

# Module Contracts

Une commande appartient toujours à un projet.

Une commande peut contenir :

plusieurs tâches

plusieurs documents

plusieurs coûts

plusieurs risques

---

# Module Tasks

Une tâche peut être liée :

à un projet

à une commande

à un responsable

à une discipline

à une phase

à des documents

à un futur planning projet

Les dépendances entre tâches seront gérées dans :

planning_project.

---

# Module Planning

Le module **planning** (Suivi des tâches) ne possède pas de modèle spécifique.

Il exploite directement :

Projects

Contracts

Tasks

Son rôle est de produire des vues consolidées.

---

# Module Planning Project

Le module **planning_project** possède ses propres modèles.

Exemples

Planning

Baseline

Version

Calendrier

Ressource

Dépendance

Contrainte

Chemin critique

Ces objets complètent les tâches mais ne les remplacent pas.

---

# Module Documents

Les documents sont liés :

aux projets

aux commandes

aux tâches

aux workflows

aux transmittals

aux conteneurs GED

---

# Module Costs

Les coûts sont liés :

aux projets

aux commandes

aux tâches

Ils alimentent :

EVM

Reporting

Dashboard

---

# Module Risks

Les risques sont liés :

aux projets

aux commandes

aux tâches

Ils alimentent :

Reporting

Dashboard

---

# Module Reporting

Le module Reporting ne stocke quasiment aucune donnée métier.

Il consolide les informations provenant des autres modules.

---

# Intégrité

Toute suppression doit préserver la cohérence de la base.

Les clés étrangères doivent utiliser le comportement adapté :

CASCADE

PROTECT

SET_NULL

selon le contexte métier.

---

# Évolutivité

La base est conçue pour intégrer de nouveaux modules :

Qualité

HSE

Inspection

Maintenance

Construction

Commissioning

Punch List

Handover

sans remise en cause du modèle existant.

---

# Sauvegardes

La base doit pouvoir être sauvegardée indépendamment des documents GED.

Les sauvegardes doivent être compatibles avec les outils PostgreSQL standards.

---

# Philosophie

La base de données constitue la source unique de vérité de PMO EPC Platform.

Les modèles doivent rester simples, normalisés et pérennes.

La logique métier appartient aux services, pas aux tables.

Chaque nouvelle table doit pouvoir s'intégrer naturellement dans l'architecture existante sans créer de dépendances inutiles ni de duplications.