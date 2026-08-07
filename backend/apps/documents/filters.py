"""
Filtres du module Documents.
Adapté à la structure réelle de la table documents_document.
"""

import django_filters
from django import forms
from django.db.models import Q

from .models import Document
from apps.projects.models import Projet
from apps.contracts.models import Commande
from apps.core_ref.models import (
    Phase, Discipline, DocTypeTechnique,
    ClasseDocumentaire, StatutCycleVie, Originator
)


class DocumentFilter(django_filters.FilterSet):
    """
    Filtre pour les documents.
    Basé sur les colonnes réelles de la table documents_document.
    """

    # ======================================================
    # RECHERCHE GÉNÉRALE
    # ======================================================

    q = django_filters.CharFilter(
        method="filter_search",
        label="Recherche",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Code, titre, description..."
        })
    )

    # ======================================================
    # FILTRES RÉFÉRENTIELS
    # ======================================================

    statut_actuel = django_filters.ModelChoiceFilter(
        queryset=StatutCycleVie.objects.all(),
        empty_label="Tous les statuts",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    classe = django_filters.ModelChoiceFilter(
        queryset=ClasseDocumentaire.objects.all(),
        empty_label="Toutes classes",
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Classe documentaire"
    )

    projet = django_filters.ModelChoiceFilter(
        queryset=Projet.objects.filter(est_generique=False),
        empty_label="Tous les projets",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    commande = django_filters.ModelChoiceFilter(
        queryset=Commande.objects.all(),
        empty_label="Toutes commandes",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    phase = django_filters.ModelChoiceFilter(
        queryset=Phase.objects.filter(actif=True),
        empty_label="Toutes phases",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    discipline = django_filters.ModelChoiceFilter(
        queryset=Discipline.objects.filter(actif=True),
        empty_label="Toutes disciplines",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    type_doc = django_filters.ModelChoiceFilter(
        queryset=DocTypeTechnique.objects.filter(actif=True),
        empty_label="Tous les types",
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Type de document"
    )

    origine = django_filters.ModelChoiceFilter(
        queryset=Originator.objects.filter(actif=True),
        empty_label="Tous les émetteurs",
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Originator"
    )

    # ======================================================
    # FILTRES BOOLÉENS
    # ======================================================

    est_archive = django_filters.BooleanFilter(
        label="Documents archivés uniquement",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = Document
        fields = [
            'q', 'statut_actuel', 'classe',
            'projet', 'commande', 'phase', 'discipline',
            'type_doc', 'origine', 'est_archive',
        ]

    # ======================================================
    # MÉTHODES PERSONNALISÉES
    # ======================================================

    def filter_search(self, queryset, name, value):
        """
        Recherche globale sur plusieurs champs.
        """
        if not value:
            return queryset

        return queryset.filter(
            Q(code_documentaire__icontains=value)
            | Q(titre__icontains=value)
            | Q(description__icontains=value)
            | Q(revision_actuelle__icontains=value)
        )