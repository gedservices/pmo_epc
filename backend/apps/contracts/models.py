from django.db import models

# Create your models here.

from django.db import models
from apps.accounts.models import User, Entite
from apps.core_ref.models import Phase, Pays, Site, Secteur


class Commande(models.Model):
    STATUT_CHOICES = [
        ('Ouvert',    'Ouvert'),
        ('En cours',  'En cours'),
        ('En attente','En attente'),
        ('Suspendu',  'Suspendu'),
        ('Terminée',  'Terminée'),
        ('Annulée',   'Annulée'),
    ]
    PRIORITE_CHOICES = [
        ('Critique','Critique'),('Haute','Haute'),
        ('Moyenne','Moyenne'),('Basse','Basse'),
    ]

    projet            = models.ForeignKey('projects.Projet',
                          on_delete=models.CASCADE, related_name='commandes')
    code_commande     = models.CharField(max_length=50, unique=True)
    code_originator   = models.CharField(max_length=4)
    nom               = models.CharField(max_length=255)
    description       = models.TextField(blank=True)
    contractor        = models.CharField(max_length=255, blank=True)
    entite_contractor = models.ForeignKey(Entite, on_delete=models.SET_NULL,
                          null=True, blank=True)
    phase             = models.ForeignKey(Phase, on_delete=models.SET_NULL,
                          null=True, blank=True)
    statut            = models.CharField(max_length=30, choices=STATUT_CHOICES,
                          default='Ouvert')
    priorite          = models.CharField(max_length=30, choices=PRIORITE_CHOICES,
                          blank=True)
    responsable       = models.ForeignKey(User, on_delete=models.SET_NULL,
                          null=True, blank=True, related_name='commandes')
    pays              = models.ForeignKey(Pays, on_delete=models.SET_NULL,
                          null=True, blank=True)
    site              = models.ForeignKey(Site, on_delete=models.SET_NULL,
                          null=True, blank=True)
    secteur           = models.ForeignKey(Secteur, on_delete=models.SET_NULL,
                          null=True, blank=True)
    date_debut_prevue = models.DateField(null=True, blank=True)
    date_fin_prevue   = models.DateField(null=True, blank=True)
    date_debut_reelle = models.DateField(null=True, blank=True)
    date_fin_reelle   = models.DateField(null=True, blank=True)
    budget_prevu      = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    budget_reel       = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    poids             = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    progression_calculee = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    duree_revue_company_defaut    = models.IntegerField(default=15)
    duree_revue_contractor_defaut = models.IntegerField(default=15)
    planned_value     = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    earned_value      = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    actual_cost       = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    est_generique     = models.BooleanField(default=False)
    date_creation     = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    cree_par          = models.ForeignKey(User, on_delete=models.SET_NULL,
                          null=True, blank=True, related_name='commandes_crees')
    modifie_par       = models.ForeignKey(User, on_delete=models.SET_NULL,
                          null=True, blank=True, related_name='commandes_modifies')

    class Meta:
        verbose_name = 'Commande'
        ordering = ['projet', 'code_commande']

    def __str__(self):
        return f"{self.code_commande} — {self.nom}"
