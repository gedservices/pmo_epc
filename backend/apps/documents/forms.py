from django import forms
from .models import Document, DocumentRevision
from apps.core_ref.models import Discipline, Phase, ClasseDocumentaire, DocTypeTechnique, Originator

# class DocumentForm(forms.ModelForm):
#     class Meta:
#         model = Document
#         fields = ['titre', 'description', 'discipline', 'phase', 'classe', 'type_doc', 'origine', 'responsable']
#         widgets = {
#             'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du document'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description technique...'}),
#             'discipline': forms.Select(attrs={'class': 'form-select'}),
#             'phase': forms.Select(attrs={'class': 'form-select'}),
#             'classe': forms.Select(attrs={'class': 'form-select'}),
#             'type_doc': forms.Select(attrs={'class': 'form-select'}),
#             'origine': forms.Select(attrs={'class': 'form-select'}),
#             'responsable': forms.Select(attrs={'class': 'form-select'}),
#         }


class DocumentForm(forms.ModelForm):
    """
    Formulaire création/modification document.
    """

    class Meta:
        model = Document
        fields = [
            'code_documentaire', 'titre', 'description',
            'revision_actuelle',
            'classe', 'type_doc', 'origine',
            'projet', 'commande', 'phase', 'discipline',
            'responsable', 'statut_actuel',
        ]
        widgets = {
            'code_documentaire': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: PID-001-A"
            }),
            'titre': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            'revision_actuelle': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: rev00"
            }),
            'classe': forms.Select(attrs={"class": "form-select"}),
            'type_doc': forms.Select(attrs={"class": "form-select"}),
            'origine': forms.Select(attrs={"class": "form-select"}),
            'projet': forms.Select(attrs={"class": "form-select"}),
            'commande': forms.Select(attrs={"class": "form-select"}),
            'phase': forms.Select(attrs={"class": "form-select"}),
            'discipline': forms.Select(attrs={"class": "form-select"}),
            'responsable': forms.Select(attrs={"class": "form-select"}),
            'statut_actuel': forms.Select(attrs={"class": "form-select"}),
        }

class DocumentUploadForm(forms.Form):
    revision = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: A, B, 00, ASB'}))
    fichier = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    code_retour = forms.ChoiceField(
        choices=[
            ('', '-- Sélectionner --'),
            ('Accepté sans commentaire', 'Accepté sans commentaire'),
            ('Accepté avec commentaire', 'Accepté avec commentaire'),
            ('Rejeté', 'Rejeté'),
            ('En révision', 'En révision'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    commentaire = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Commentaire technique...'}))