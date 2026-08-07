from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone
from apps.accounts.models import User
from apps.core_ref.models import Phase, Discipline


class Tache(models.Model):
    STATUT_CHOICES = [
        ('En attente', 'En attente'),
        ('En cours',   'En cours'),
        ('Terminée',   'Terminée'),
        ('Suspendue',  'Suspendue'),
        ('Annulée',    'Annulée'),
    ]

    projet      = models.ForeignKey(
        'projects.Projet', on_delete=models.CASCADE,
        related_name='taches')
    commande    = models.ForeignKey(
        'contracts.Commande', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='taches')

    nom         = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    phase       = models.ForeignKey(Phase, on_delete=models.SET_NULL,
                                    null=True, blank=True)
    discipline  = models.ForeignKey(Discipline, on_delete=models.SET_NULL,
                                    null=True, blank=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name='taches')

    statut      = models.CharField(max_length=30, choices=STATUT_CHOICES,
                                   default='En attente')
    poids       = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    avancement  = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    date_debut_prevue = models.DateField(null=True, blank=True)
    date_fin_prevue   = models.DateField(null=True, blank=True)
    date_debut_reelle = models.DateField(null=True, blank=True)
    date_fin_reelle   = models.DateField(null=True, blank=True)

    cout_prevu  = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cout_reel   = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    # EVM
    planned_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    earned_value  = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    actual_cost   = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    est_en_retard = models.BooleanField(default=False)
    est_jalon     = models.BooleanField(default=False)

    date_creation     = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    cree_par          = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='taches_crees')
    modifie_par       = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='taches_modifies')

    class Meta:
        verbose_name = 'Tâche'
        ordering = ['projet', 'commande', 'date_debut_prevue']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        # Recalcul est_en_retard
        if (self.date_fin_prevue and
                self.date_fin_prevue < timezone.now().date() and
                self.avancement < 100):
            self.est_en_retard = True
        else:
            self.est_en_retard = False
        super().save(*args, **kwargs)

    @property
    def couleur_statut(self):
        return {
            'En cours':   'warning',
            'Terminée':   'success',
            'En attente': 'info',
            'Suspendue':  'secondary',
            'Annulée':    'danger',
        }.get(self.statut, 'secondary')

    @property
    def couleur_avancement(self):
        a = float(self.avancement)
        if a >= 70:   return 'success'
        if a >= 30:   return 'warning'
        return 'danger'


class HistoriqueTache(models.Model):
    tache             = models.ForeignKey(Tache, on_delete=models.CASCADE,
                                          related_name='historique')
    champ_modifie     = models.CharField(max_length=50)
    ancienne_valeur   = models.TextField(blank=True)
    nouvelle_valeur   = models.TextField(blank=True)
    date_modification = models.DateTimeField(auto_now_add=True)
    modifie_par       = models.ForeignKey(User, on_delete=models.SET_NULL,
                                          null=True)

    class Meta:
        ordering = ['-date_modification']