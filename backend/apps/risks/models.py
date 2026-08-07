from django.db import models

# Create your models here.

from django.db import models
from apps.accounts.models import User


class Risque(models.Model):
    STATUT_CHOICES = [
        ('Ouvert',   'Ouvert'),
        ('En cours', 'En cours'),
        ('Clôturé',  'Clôturé'),
        ('Accepté',  'Accepté'),
    ]

    projet      = models.ForeignKey(
        'projects.Projet', on_delete=models.CASCADE,
        related_name='risques')
    commande    = models.ForeignKey(
        'contracts.Commande', on_delete=models.CASCADE,
        null=True, blank=True, related_name='risques')

    titre       = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    probabilite = models.IntegerField()
    impact      = models.IntegerField()

    statut      = models.CharField(max_length=30, choices=STATUT_CHOICES,
                                   default='Ouvert')
    plan_mitigation  = models.TextField(blank=True)
    responsable      = models.ForeignKey(User, on_delete=models.SET_NULL,
                                         null=True, blank=True)
    date_identification = models.DateField(auto_now_add=True)
    date_echeance       = models.DateField(null=True, blank=True)
    date_creation       = models.DateTimeField(auto_now_add=True)
    date_modification   = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Risque'
        ordering = ['-probabilite', '-impact']

    def __str__(self):
        return self.titre

    @property
    def criticite(self):
        return self.probabilite * self.impact

    @property
    def niveau_criticite(self):
        c = self.criticite
        if c >= 15: return ('danger',   'Critique')
        if c >= 9:  return ('warning',  'Élevé')
        if c >= 4:  return ('info',     'Modéré')
        return             ('success',  'Faible')

    @property
    def couleur_cellule(self):
        c = self.criticite
        if c >= 15: return '#ffcdd2'
        if c >= 9:  return '#fff3cd'
        if c >= 4:  return '#d1ecf1'
        return             '#d4edda'
