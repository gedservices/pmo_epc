"""
Filtres du module Contracts.

Utilisation avec django-filter.

Permet de filtrer les commandes par :
    - recherche texte
    - statut
    - priorité
    - phase
    - projet
    - contractor
"""

import django_filters
from django import forms
from .models import Commande
from apps.projects.models import Projet
from apps.core_ref.models import Phase


class CommandeFilter(django_filters.FilterSet):
    """
    Filtre pour les commandes.
    Compatible avec le nouveau design PMO EPC.
    """

    # ======================================================
    # RECHERCHE GENERALE
    # ======================================================

    q = django_filters.CharFilter(
        method="filter_search",
        label="Recherche",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Code, nom, contractor..."
            }
        )
    )

    # ======================================================
    # FILTRES REFERENTIELS
    # ======================================================

    statut = django_filters.ChoiceFilter(
        choices=Commande.STATUT_CHOICES,
        empty_label="Tous les statuts",
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    priorite = django_filters.ChoiceFilter(
        choices=Commande.PRIORITE_CHOICES,
        empty_label="Toutes priorités",
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    phase = django_filters.ModelChoiceFilter(
        queryset=Phase.objects.all(),
        empty_label="Toutes phases",
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    projet = django_filters.ModelChoiceFilter(
        queryset=Projet.objects.all(),
        empty_label="Tous les projets",
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    class Meta:
        model = Commande
        fields = [
            "q",
            "statut",
            "priorite",
            "phase",
            "projet",
        ]

    # ======================================================
    # METHODES PERSONNALISEES
    # ======================================================

    def filter_search(self, queryset, name, value):
        """
        Recherche globale sur plusieurs champs.
        """
        if not value:
            return queryset

        from django.db.models import Q

        return queryset.filter(
            Q(code_commande__icontains=value)
            |
            Q(nom__icontains=value)
            |
            Q(contractor__icontains=value)
            |
            Q(description__icontains=value)
        )