from django import forms

from .models import Risque


class RisqueForm(forms.ModelForm):

    class Meta:
        model = Risque

        fields = [
            "projet",
            "commande",
            "titre",
            "description",
            "probabilite",
            "impact",
            "statut",
            "plan_mitigation",
            "responsable",
            "date_echeance",
        ]

        widgets = {

            "projet": forms.Select(attrs={
                "class": "form-select",
            }),

            "commande": forms.Select(attrs={
                "class": "form-select",
            }),

            "titre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Titre du risque",
                "maxlength": 255,
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
            }),

            "probabilite": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 5,
            }),

            "impact": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 5,
            }),

            "statut": forms.Select(attrs={
                "class": "form-select",
            }),

            "plan_mitigation": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Décrire les actions de mitigation...",
            }),

            "responsable": forms.Select(attrs={
                "class": "form-select",
            }),

            "date_echeance": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        probabilite = cleaned_data.get("probabilite")
        impact = cleaned_data.get("impact")

        if probabilite is not None:
            if probabilite < 1 or probabilite > 5:
                self.add_error(
                    "probabilite",
                    "La probabilité doit être comprise entre 1 et 5."
                )

        if impact is not None:
            if impact < 1 or impact > 5:
                self.add_error(
                    "impact",
                    "L'impact doit être compris entre 1 et 5."
                )

        return cleaned_data