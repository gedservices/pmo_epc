from django import forms

from .models import Tache


class TacheForm(forms.ModelForm):

    class Meta:
        model = Tache

        fields = [
            "projet",
            "commande",
            "nom",
            "description",
            "phase",
            "discipline",
            "responsable",
            "statut",
            "poids",
            "avancement",
            "date_debut_prevue",
            "date_fin_prevue",
            "date_debut_reelle",
            "date_fin_reelle",
            "cout_prevu",
            "cout_reel",
            "planned_value",
            "earned_value",
            "actual_cost",
            "est_jalon",
        ]

        widgets = {

            "projet": forms.Select(attrs={
                "class": "form-select",
            }),

            "commande": forms.Select(attrs={
                "class": "form-select",
            }),

            "nom": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nom de la tâche",
                "maxlength": 255,
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
            }),

            "phase": forms.Select(attrs={
                "class": "form-select",
            }),

            "discipline": forms.Select(attrs={
                "class": "form-select",
            }),

            "responsable": forms.Select(attrs={
                "class": "form-select",
            }),

            "statut": forms.Select(attrs={
                "class": "form-select",
            }),

            "poids": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0",
            }),

            "avancement": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0",
                "max": "100",
            }),

            "date_debut_prevue": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),

            "date_fin_prevue": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),

            "date_debut_reelle": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),

            "date_fin_reelle": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),

            "cout_prevu": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
            }),

            "cout_reel": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
            }),

            "planned_value": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
            }),

            "earned_value": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
            }),

            "actual_cost": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
            }),

            "est_jalon": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        debut_prev = cleaned_data.get("date_debut_prevue")
        fin_prev = cleaned_data.get("date_fin_prevue")

        if debut_prev and fin_prev:
            if fin_prev < debut_prev:
                self.add_error(
                    "date_fin_prevue",
                    "La date de fin prévue doit être postérieure à la date de début prévue."
                )

        debut_reel = cleaned_data.get("date_debut_reelle")
        fin_reel = cleaned_data.get("date_fin_reelle")

        if debut_reel and fin_reel:
            if fin_reel < debut_reel:
                self.add_error(
                    "date_fin_reelle",
                    "La date de fin réelle doit être postérieure à la date de début réelle."
                )

        avancement = cleaned_data.get("avancement")

        if avancement is not None:
            if avancement < 0 or avancement > 100:
                self.add_error(
                    "avancement",
                    "L'avancement doit être compris entre 0 et 100 %."
                )

        poids = cleaned_data.get("poids")

        if poids is not None and poids < 0:
            self.add_error(
                "poids",
                "Le poids ne peut pas être négatif."
            )

        return cleaned_data