"""
Filtres du module Projects.

Utilisation avec django-filter.

Permet de filtrer les projets par :
    - recherche texte
    - statut
    - priorité
    - responsable
    - conteneur
    - organisation
    - dates
    - retard
"""

import django_filters

from django import forms

from .models import Projet

from apps.accounts.models import User, Entite

from apps.core_ref.models import (
    Conteneur,
    Pays,
    Site,
    Secteur,
)



class ProjetFilter(django_filters.FilterSet):


    # ======================================================
    # RECHERCHE GENERALE
    # ======================================================

    q = django_filters.CharFilter(
        method="filter_search",
        label="Recherche",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder":
                    "Code, nom, description..."
            }
        )
    )


    # ======================================================
    # FILTRES REFERENTIELS
    # ======================================================

    statut = django_filters.ChoiceFilter(
        choices=Projet.STATUT_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )


    priorite = django_filters.ChoiceFilter(
        choices=Projet.PRIORITE_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )


    conteneur = django_filters.ModelChoiceFilter(
        queryset=Conteneur.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )


    responsable = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )


    entite = django_filters.ModelChoiceFilter(
        queryset=Entite.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )


    pays = django_filters.ModelChoiceFilter(
        queryset=Pays.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )


    site = django_filters.ModelChoiceFilter(
        queryset=Site.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )


    secteur = django_filters.ModelChoiceFilter(
        queryset=Secteur.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )



    # ======================================================
    # FILTRE RETARD
    # ======================================================

    retard = django_filters.BooleanFilter(
        method="filter_retard",
        label="Projet en retard",
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input"
            }
        )
    )



    # ======================================================
    # FILTRE DATES
    # ======================================================

    date_fin_prevue = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(
            attrs={
                "type": "date",
                "class": "form-control"
            }
        )
    )



    class Meta:

        model = Projet

        fields = [
            "q",
            "statut",
            "priorite",
            "conteneur",
            "responsable",
            "entite",
            "pays",
            "site",
            "secteur",
            "retard",
            "date_fin_prevue",
        ]



    # ======================================================
    # METHODES PERSONNALISEES
    # ======================================================

    def filter_search(self, queryset, name, value):

        if not value:
            return queryset


        from django.db.models import Q


        return queryset.filter(

            Q(code__icontains=value)

            |

            Q(nom__icontains=value)

            |

            Q(description__icontains=value)

            |

            Q(type_projet__icontains=value)

        )



    def filter_retard(self, queryset, name, value):

        if value is None:
            return queryset


        projets = []


        for projet in queryset:

            if projet.est_en_retard == value:
                projets.append(projet.pk)


        return queryset.filter(
            pk__in=projets
        )