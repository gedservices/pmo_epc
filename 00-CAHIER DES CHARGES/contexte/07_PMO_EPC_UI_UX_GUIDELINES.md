# PMO EPC Platform

# UI / UX Guidelines

Version : 2.0

---

# Objectif

Ce document définit les règles de conception des interfaces utilisateur de PMO EPC Platform.

Il garantit que tous les modules présentent :

- la même ergonomie
- les mêmes composants
- les mêmes conventions
- les mêmes comportements

Quel que soit le module développé, l'utilisateur doit immédiatement retrouver ses repères.

---

# Philosophie

PMO EPC Platform est un logiciel métier destiné :

- aux chefs de projet
- aux PMO
- aux ingénieurs
- aux document controllers
- aux planificateurs
- aux acheteurs
- aux responsables de contrats

L'objectif n'est pas de réaliser une interface spectaculaire mais une interface :

✓ rapide

✓ dense

✓ lisible

✓ homogène

✓ productive

---

# Principe général

Une page doit répondre immédiatement à trois questions :

Où suis-je ?

Que puis-je faire ?

Quel est l'état actuel ?

---

# Structure générale

Toutes les pages utilisent exactement la même structure.

```
Sidebar

Topbar

Breadcrumb

Titre

Description

Toolbar

Filtres

Statistiques

Contenu

Pagination

Footer
```

Aucune exception.

---

# Sidebar

Organisation officielle.

```
Dashboard

Portefeuille

    Projets

    Commandes

Exécution

    Tâches

Suivi Planning

    Gantt Projets

    Suivi des tâches

Planification

    Planning Projects

Pilotage

    Coûts

    Risques

GED

    Documents

Reporting

    Reporting

    EVM

Administration

    Utilisateurs

    Référentiels
```

Les intitulés doivent rester stables.

---

# Topbar

La topbar contient uniquement :

Recherche globale

Notifications

Utilisateur

Déconnexion

Jamais de logique métier.

---

# Breadcrumb

Toutes les pages de niveau 2 ou plus affichent un fil d'Ariane.

Exemple

```
Accueil

>

Projets

>

Projet ABC

>

Commande XYZ
```

---

# Titre

Chaque page possède :

Titre

Description

Actions

Exemple

```
Suivi des tâches

Visualisation consolidée des tâches du portefeuille.

[Nouvelle tâche]
```

---

# Toolbar

Toujours présente.

Contient :

Recherche

Export

Actualiser

Imprimer

Création

Actions globales

---

# Filtres

Toujours affichés sous la toolbar.

Organisation recommandée.

```
Projet

Commande

Responsable

Discipline

Phase

Statut

Période
```

Les filtres les plus utilisés apparaissent en premier.

---

# Cartes statistiques

Toutes les listes commencent par des indicateurs.

Exemple

```
Nombre de tâches

Avancement

Retards

Jalons

Coût

Charge
```

Maximum :

8 cartes

---

# Couleurs

Palette officielle.

Primaire

Bleu

Succès

Vert

Avertissement

Orange

Erreur

Rouge

Information

Bleu clair

Secondaire

Gris

Aucune autre couleur métier.

---

# Icônes

Bootstrap Icons uniquement.

Les mêmes objets utilisent toujours la même icône.

Projet

folder2-open

Commande

file-earmark-text

Document

folder

Tâche

check2-square

Planning

calendar3

Risque

exclamation-triangle

Coût

currency-euro

Reporting

graph-up-arrow

Administration

gear

---

# Boutons

Ordre officiel.

Retour

Annuler

Enregistrer

Créer

Supprimer

Le bouton principal est toujours situé à droite.

---

# Listes

Structure obligatoire.

```
Toolbar

Filtres

Statistiques

Tableau

Pagination
```

---

# Tableaux

Tous les tableaux utilisent les composants communs.

Colonnes :

alignées

triables

filtrables

Actions toujours à droite.

---

# Formulaires

Tous les formulaires suivent le même découpage.

Informations générales

Organisation

Planning

Budget

Commentaires

Historique

Les sections utilisent les composants communs.

---

# Pages de détail

Organisation.

```
En-tête

Résumé

Informations

Sections

Historique

Documents liés

Commentaires
```

---

# Dashboard

Structure.

```
Indicateurs

Graphiques

Alertes

Tableaux

Activité récente
```

---

# Gantt

Toujours constitué de deux zones.

```
Arborescence

Diagramme
```

Synchronisation verticale obligatoire.

---

# Calendrier

Modes disponibles.

Jour

Semaine

Mois

Agenda

---

# Charge

Présentation.

```
Responsable

Capacité

Charge

Disponibilité

Surcharge
```

Utiliser des barres de progression.

---

# Retards

Afficher :

Retard

Cause

Responsable

Impact

Nombre de jours

Priorité

---

# Jalons

Différencier visuellement :

Projet

Commande

Planning

Documentaire

Contractuel

Technique

---

# Progression

Toujours représentée :

barre

+

pourcentage

Jamais uniquement un nombre.

---

# États

Tous les statuts utilisent les badges communs.

Ne jamais recréer de badges.

---

# États vides

Toutes les pages utilisent le composant Empty State.

Il doit proposer :

Créer

Importer

Actualiser

---

# Confirmations

Toutes les confirmations utilisent le même composant.

Aucune fenêtre spécifique.

---

# Responsive

Priorité Desktop.

Ensuite :

Tablette.

Le mobile est secondaire.

---

# Performance

Limiter :

animations

chargements

rafraîchissements

Les tableaux volumineux doivent être paginés.

---

# Accessibilité

Contrastes élevés.

Texte lisible.

Navigation clavier.

Messages explicites.

Icônes accompagnées d'un libellé.

---

# Réutilisation

Les composants doivent provenir exclusivement de :

```
templates/base/components/
```

Toute duplication est interdite.

---

# Organisation des composants

```
cards/

tables/

detail/

forms/

widgets/

badges/

progress/

states/

workspace/

plannings/
```

Tout nouveau composant doit être placé dans l'un de ces dossiers.

---

# Composants Planning

Les modules :

Suivi des tâches

Planning Project

partagent les mêmes composants graphiques.

Ils ne diffèrent que par leurs données.

---

# Cohérence

Deux pages affichant la même information doivent utiliser :

la même icône

la même couleur

le même tableau

les mêmes boutons

les mêmes badges

---

# Règle fondamentale

L'utilisateur ne doit jamais avoir à réapprendre l'interface lorsqu'il change de module.

La cohérence de l'expérience utilisateur est considérée comme une fonctionnalité à part entière de PMO EPC Platform.