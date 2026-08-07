from django.db import models

# Create your models here.

from django.db import models
from apps.accounts.models import User

class Cout(models.Model):
    projet    = models.ForeignKey('projects.Projet', on_delete=models.CASCADE,
                  related_name='couts')
    commande  = models.ForeignKey('contracts.Commande', on_delete=models.CASCADE,
                  null=True, blank=True, related_name='couts')
    tache     = models.ForeignKey('tasks.Tache', on_delete=models.SET_NULL,
                  null=True, blank=True)
    libelle   = models.CharField(max_length=255)
    categorie = models.CharField(max_length=100, blank=True)
    cout_prevu = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cout_reel  = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    date_cout  = models.DateField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    cree_par   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Coût'
        ordering = ['-date_cout']

    def __str__(self): return self.libelle

    @property
    def derive(self): return float(self.cout_reel) - float(self.cout_prevu)
