from django import forms

from apps.projects.models import Projet
from apps.core_ref.models import Discipline, Phase


class PlanningFilterForm(forms.Form):

    projet = forms.ModelChoiceField(
        queryset=Projet.objects.filter(est_generique=False),
        required=False
    )

    phase = forms.ModelChoiceField(
        queryset=Phase.objects.all(),
        required=False
    )

    discipline = forms.ModelChoiceField(
        queryset=Discipline.objects.all(),
        required=False
    )

    responsable = forms.CharField(
        required=False
    )

    afficher_jalons = forms.BooleanField(
        required=False
    )

    afficher_terminees = forms.BooleanField(
        required=False
    )