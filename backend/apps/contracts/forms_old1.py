from django import forms

from .models import Commande


class CommandeForm(forms.ModelForm):

    class Meta:

        model = Commande

        exclude = [
            "date_creation",
            "date_modification",
            "cree_par",
            "modifie_par",
        ]

        widgets = {

            "description": forms.Textarea(
                attrs={"rows": 4}
            ),

            "date_debut_prevue": forms.DateInput(
                attrs={"type": "date"}
            ),

            "date_fin_prevue": forms.DateInput(
                attrs={"type": "date"}
            ),

            "date_debut_reelle": forms.DateInput(
                attrs={"type": "date"}
            ),

            "date_fin_reelle": forms.DateInput(
                attrs={"type": "date"}
            ),

        }