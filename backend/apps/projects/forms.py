from django import forms
from .models import Projet
from apps.accounts.models import User, Entite
from apps.core_ref.models import Pays, Site, Secteur, Conteneur


class ProjetForm(forms.ModelForm):
    class Meta:
        model  = Projet
        fields = [
            'code', 'nom', 'description', 'type_projet',
            'conteneur', 'statut', 'priorite',
            'responsable', 'entite',
            'pays', 'site', 'secteur',
            'date_debut_prevue', 'date_fin_prevue',
            'date_debut_reelle', 'date_fin_reelle',
            'budget_prevu', 'budget_reel',
            'planned_value', 'earned_value', 'actual_cost',
        ]
        widgets = {
            'code':        forms.TextInput(attrs={'class': 'form-control'}),
            'nom':         forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                               'class': 'form-control', 'rows': 3}),
            'type_projet': forms.TextInput(attrs={'class': 'form-control'}),
            'conteneur':   forms.Select(attrs={'class': 'form-select'}),
            'statut':      forms.Select(attrs={'class': 'form-select'}),
            'priorite':    forms.Select(attrs={'class': 'form-select'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'entite':      forms.Select(attrs={'class': 'form-select'}),
            'pays':        forms.Select(attrs={'class': 'form-select'}),
            'site':        forms.Select(attrs={'class': 'form-select'}),
            'secteur':     forms.Select(attrs={'class': 'form-select'}),
            'date_debut_prevue': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_prevue':   forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}),
            'date_debut_reelle': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_reelle':   forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}),
            'budget_prevu':  forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}),
            'budget_reel':   forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}),
            'planned_value': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}),
            'earned_value':  forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}),
            'actual_cost':   forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}),
        }