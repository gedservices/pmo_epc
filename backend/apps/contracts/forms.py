from django import forms

from .models import Commande


class CommandeForm(forms.ModelForm):

    class Meta:

        model = Commande

        fields = [

            "projet",

            "code_commande",
            "code_originator",
            "nom",
            "description",

            "contractor",
            "entite_contractor",

            "phase",

            "statut",
            "priorite",

            "responsable",

            "pays",
            "site",
            "secteur",

            "date_debut_prevue",
            "date_fin_prevue",

            "budget_prevu",
            "budget_reel",

            "poids",

        ]


        labels = {

            "projet": "Projet",

            "code_commande": "Code Commande",

            "code_originator": "Code Originateur",

            "nom": "Nom de la commande",

            "description": "Description",

            "contractor": "Contractor",

            "entite_contractor": "Entité Contractor",

            "phase": "Phase Projet",

            "statut": "Statut",

            "priorite": "Priorité",

            "responsable": "Responsable",

            "pays": "Pays",

            "site": "Site",

            "secteur": "Secteur",

            "date_debut_prevue": "Date début prévue",

            "date_fin_prevue": "Date fin prévue",

            "budget_prevu": "Budget prévu",

            "budget_reel": "Budget réel",

            "poids": "Poids dans le projet",

        }



        widgets = {


            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Description de la commande"
                }
            ),


            "date_debut_prevue": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),


            "date_fin_prevue": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),


            "budget_prevu": forms.NumberInput(
                attrs={
                    "placeholder": "Montant prévu"
                }
            ),


            "budget_reel": forms.NumberInput(
                attrs={
                    "placeholder": "Montant réel"
                }
            ),


            "poids": forms.NumberInput(
                attrs={
                    "placeholder": "Poids (%)",
                    "step": "0.01"
                }
            ),


            "code_commande": forms.TextInput(
                attrs={
                    "placeholder": "Ex : CMD-001"
                }
            ),


            "code_originator": forms.TextInput(
                attrs={
                    "placeholder": "Ex : ABC"
                }
            ),


            "nom": forms.TextInput(
                attrs={
                    "placeholder": "Nom de la commande"
                }
            ),


            "contractor": forms.TextInput(
                attrs={
                    "placeholder": "Nom du contractor"
                }
            ),


        }



    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        for field_name, field in self.fields.items():

            widget = field.widget


            if isinstance(
                widget,
                (
                    forms.TextInput,
                    forms.NumberInput,
                    forms.DateInput,
                    forms.Select,
                    forms.Textarea,
                )
            ):

                widget.attrs.update(
                    {
                        "class": "form-control"
                    }
                )