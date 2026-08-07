# PMO EPC Platform

# Component Library

Version : 1.0

---

# Objectif

Ce document décrit l'ensemble des composants graphiques réutilisables de PMO EPC Platform.

Tous les nouveaux développements doivent utiliser ces composants avant d'en créer de nouveaux.

La bibliothèque constitue le socle graphique officiel de la plateforme.

---

# Organisation

Les composants sont centralisés dans :

```
templates/base/components/
```

Organisation actuelle :

```
badges/

cards/

detail/

forms/

plannings/

progress/

states/

tables/

widgets/

workspace/
```

---

# Principe

Les composants doivent être :

- indépendants
- réutilisables
- simples
- documentés

Ils ne doivent jamais contenir de logique métier.

Ils ne servent qu'à présenter des données.

---

# Cards

Répertoire

```
components/cards/
```

---

## card.html

Carte Bootstrap standard.

Utilisation :

- blocs d'information
- formulaires
- statistiques
- tableaux

---

## card_section.html

Section interne d'une carte.

Utilisation :

- découpage logique
- séparation visuelle

---

## object_header.html

En-tête d'un objet.

Affiche :

- titre
- code
- statut
- actions

Utilisé dans :

Projet

Commande

Document

Tâche

---

## section_title.html

Titre de section.

Uniformise tous les sous-titres.

---

# Badges

Répertoire

```
components/badges/
```

---

## badge_statut.html

Affiche :

- statut
- couleur

Utilisé partout.

---

## badge_priorite.html

Affiche la priorité.

---

## badge_phase.html

Affiche la phase EPC.

---

## badge_discipline.html

Affiche la discipline.

---

## badge_progression.html

Affiche le pourcentage d'avancement.

---

# Forms

Répertoire

```
components/forms/
```

---

## field.html

Champ générique.

---

## field_checkbox.html

Case à cocher.

---

## field_money.html

Champ monétaire.

---

## field_select.html

Liste déroulante.

---

## field_textarea.html

Texte long.

---

## field_date.html

Sélecteur de date.

---

## form_section_begin.html

Début d'une section.

---

## form_section_end.html

Fin d'une section.

---

## form_actions.html

Boutons standards :

Retour

Annuler

Enregistrer

---

# Tables

Répertoire

```
components/tables/
```

---

## table.html

Tableau principal.

---

## table_header.html

En-tête.

---

## table_actions.html

Colonne Actions.

---

## table_empty.html

Affiché lorsqu'aucune donnée n'existe.

---

# Detail

Répertoire

```
components/detail/
```

---

## object_header.html

En-tête des fiches détail.

---

## info_group.html

Bloc d'informations.

---

## info_row.html

Ligne d'information.

---

## progress_bar.html

Barre de progression.

---

## progress_card.html

Carte de progression.

---

## stat_card.html

Carte statistique.

---

## avatar.html

Affichage utilisateur.

---

## linked_object.html

Lien vers un objet associé.

---

## document_counter.html

Compteur documentaire.

---

## timeline_item.html

Élément d'historique.

---

## section_title.html

Titre de section.

---

# Progress

Répertoire

```
components/progress/
```

---

## progress_bar.html

Affiche :

barre

+

pourcentage

Composant officiel.

---

# States

Répertoire

```
components/states/
```

---

## empty.html

Aucune donnée.

---

## empty_state.html

État vide illustré.

Utilisé par toutes les listes.

---

# Widgets

Répertoire

```
components/widgets/
```

---

## toolbar.html

Toolbar standard.

---

## filters.html

Filtres.

---

## searchbar.html

Recherche.

---

## pagination.html

Pagination.

---

## datatable.html

Configuration DataTable.

---

## modal_confirm.html

Fenêtre de confirmation.

---

## loading_spinner.html

Chargement.

---

# Workspace

Répertoire

```
components/workspace/
```

---

## workspace_toolbar.html

Toolbar métier.

---

## workspace_tabs.html

Onglets.

---

# Planning

Répertoire

```
components/plannings/
```

Ces composants sont utilisés à la fois par :

- Suivi des tâches
- Planning Project

Ils constituent la bibliothèque officielle des écrans Planning.

---

## planning_header.html

En-tête.

Contient :

Titre

Description

Actions

---

## planning_toolbar.html

Toolbar Planning.

Contient :

Recherche

Export

Actualiser

---

## planning_filters.html

Filtres métier.

Projet

Commande

Responsable

Statut

Phase

Période

---

## planning_statistics.html

Cartes statistiques.

Nombre de tâches

Retards

Charge

Jalons

Progression

---

## planning_summary.html

Résumé global.

Utilisé sur le dashboard.

---

## planning_project_card.html

Résumé par projet.

---

## planning_command_card.html

Résumé par commande.

---

## planning_responsible_card.html

Résumé par responsable.

---

## planning_retards.html

Liste des retards.

---

## planning_jalons.html

Liste des jalons.

---

## planning_gantt.html

Composant Gantt.

Deux zones :

Arborescence

Diagramme

---

## planning_calendar.html

Calendrier.

Modes :

Jour

Semaine

Mois

Agenda

---

## planning_load.html

Charge.

Par :

Responsable

Discipline

Equipe

---

# Création d'un nouveau composant

Avant toute création :

1 Vérifier qu'un composant similaire n'existe pas.

2 Vérifier si le composant peut être enrichi.

3 Créer un nouveau composant uniquement si aucune solution n'existe.

---

# Convention de nommage

Toujours utiliser des noms explicites.

Exemples :

```
planning_statistics.html

badge_phase.html

workspace_tabs.html

progress_bar.html
```

Jamais :

```
card1.html

test.html

new.html

widget.html
```

---

# Dépendances

Un composant ne doit jamais dépendre :

d'un modèle Django

d'un service

d'une vue

Il dépend uniquement des données qui lui sont passées dans le contexte.

---

# Réutilisation

Les composants sont conçus pour être utilisés par plusieurs modules.

Exemple :

```
Projet

Commande

Tâche

Document

Planning

GED

Reporting
```

Le même composant doit pouvoir être réutilisé sans modification.

---

# Philosophie

La bibliothèque de composants constitue le "framework interne" de PMO EPC Platform.

Plus elle est riche et cohérente, plus les développements futurs seront rapides, homogènes et faciles à maintenir.

Tout nouveau développement doit commencer par rechercher un composant existant avant d'en créer un nouveau.