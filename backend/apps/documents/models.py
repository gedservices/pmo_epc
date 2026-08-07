from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from apps.core_ref.models import Phase, Discipline, ClasseDocumentaire, DocTypeTechnique, StatutCycleVie, SequenceStatut, Originator
from apps.projects.models import Projet
from apps.contracts.models import Commande

class Document(models.Model):
    code_documentaire = models.CharField(max_length=50, unique=True)
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='documents')
    commande = models.ForeignKey(Commande, null=True, blank=True, on_delete=models.SET_NULL, related_name='documents')
    discipline = models.ForeignKey(Discipline, null=True, blank=True, on_delete=models.SET_NULL)
    phase = models.ForeignKey(Phase, null=True, blank=True, on_delete=models.SET_NULL)
    classe = models.ForeignKey(ClasseDocumentaire, null=True, blank=True, on_delete=models.SET_NULL)
    type_doc = models.ForeignKey(DocTypeTechnique, null=True, blank=True, on_delete=models.SET_NULL)
    statut_actuel = models.ForeignKey(StatutCycleVie, null=True, on_delete=models.SET_NULL)
    revision_actuelle = models.CharField(max_length=10, default="A")
    origine = models.ForeignKey(Originator, null=True, blank=True, on_delete=models.SET_NULL)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_emission = models.DateTimeField(null=True, blank=True)
    est_archive = models.BooleanField(default=False)

    class Meta:
        db_table = 'documents_document'
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.code_documentaire} - {self.titre[:40]}"

class DocumentRevision(models.Model):
    document = models.ForeignKey(Document, related_name='revisions', on_delete=models.CASCADE)
    revision = models.CharField(max_length=10)
    statut = models.ForeignKey(StatutCycleVie, on_delete=models.PROTECT)
    fichier = models.FileField(upload_to='documents/%Y/%m/')
    code_retour = models.CharField(max_length=50, blank=True, help_text="Accepté sans commentaire / Rejeté, etc.")
    commentaire = models.TextField(blank=True)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date_emission = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_emission']

    def __str__(self):
        return f"{self.document.code_documentaire} Rev {self.revision}"
