from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from apps.accounts.models import User, Entite
from apps.core_ref.models import (Pays, Site, Secteur, Conteneur, Phase)


class Projet(models.Model):
    STATUT_CHOICES = [
        ('Ouvert',     'Ouvert'),
        ('En cours',   'En cours'),
        ('En attente', 'En attente'),
        ('Suspendu',   'Suspendu'),
        ('Clôturé',    'Clôturé'),
        ('Annulé',     'Annulé'),
        ('Finalisé',   'Finalisé'),
    ]
    PRIORITE_CHOICES = [
        ('Critique', 'Critique'),
        ('Haute',    'Haute'),
        ('Moyenne',  'Moyenne'),
        ('Basse',    'Basse'),
    ]

    code          = models.CharField(max_length=50, unique=True)
    nom           = models.CharField(max_length=255)
    description   = models.TextField(blank=True)
    type_projet   = models.CharField(max_length=50, blank=True)
    conteneur     = models.ForeignKey(Conteneur, on_delete=models.PROTECT,
                                      related_name='projets')
    statut        = models.CharField(max_length=30, choices=STATUT_CHOICES,
                                     default='Ouvert')
    priorite      = models.CharField(max_length=30, choices=PRIORITE_CHOICES,
                                     blank=True)
    responsable   = models.ForeignKey(User, on_delete=models.SET_NULL,
                                      null=True, blank=True,
                                      related_name='projets_responsable')
    entite        = models.ForeignKey(Entite, on_delete=models.SET_NULL,
                                      null=True, blank=True)
    pays          = models.ForeignKey(Pays, on_delete=models.SET_NULL,
                                      null=True, blank=True)
    site          = models.ForeignKey(Site, on_delete=models.SET_NULL,
                                      null=True, blank=True)
    secteur       = models.ForeignKey(Secteur, on_delete=models.SET_NULL,
                                      null=True, blank=True)

    # Entités et sites multiples (M2M)
    entites_associees = models.ManyToManyField(
        Entite, through='ProjetEntite',
        related_name='projets_associes', blank=True)
    sites_associes = models.ManyToManyField(
        Site, through='ProjetSite',
        related_name='projets_associes', blank=True)

    # Planning
    date_debut_prevue = models.DateField(null=True, blank=True)
    date_fin_prevue   = models.DateField(null=True, blank=True)
    date_debut_reelle = models.DateField(null=True, blank=True)
    date_fin_reelle   = models.DateField(null=True, blank=True)

    # Budget
    budget_prevu  = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    budget_reel   = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    # Avancement
    progression_calculee = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)
    poids_portefeuille   = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)

    # EVM
    planned_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    earned_value  = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    actual_cost   = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    # Flags
    est_generique     = models.BooleanField(default=False)
    est_lecture_seule = models.BooleanField(default=False)

    # Metadata
    date_creation     = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    cree_par          = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='projets_crees')
    modifie_par       = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='projets_modifies')

    class Meta:
        verbose_name = 'Projet'
        ordering = ['-date_modification']

    def __str__(self):
        return f"{self.code} — {self.nom}"

    # ── Propriétés calculées ──────────────────────────────────

    @property
    def est_en_retard(self):
        if (self.date_fin_prevue and
                self.date_fin_prevue < timezone.now().date() and
                self.progression_calculee < 100):
            return True
        return False

    @property
    def derive_budget(self):
        return float(self.budget_reel) - float(self.budget_prevu)

    @property
    def taux_consommation(self):
        if self.budget_prevu > 0:
            return round(float(self.budget_reel) /
                         float(self.budget_prevu) * 100, 1)
        return 0

    @property
    def spi(self):
        if self.planned_value > 0:
            return round(float(self.earned_value) /
                         float(self.planned_value), 3)
        return None

    @property
    def cpi(self):
        if self.actual_cost > 0:
            return round(float(self.earned_value) /
                         float(self.actual_cost), 3)
        return None

    @property
    def couleur_priorite(self):
        return {
            'Critique': 'danger',
            'Haute':    'warning',
            'Moyenne':  'info',
            'Basse':    'secondary',
        }.get(self.priorite, 'secondary')

    @property
    def couleur_statut(self):
        return {
            'En cours':   'warning',
            'Ouvert':     'info',
            'En attente': 'info',
            'Terminée':   'success',
            'Finalisé':   'success',
            'Suspendu':   'secondary',
            'Annulé':     'danger',
            'Clôturé':    'dark',
        }.get(self.statut, 'secondary')

    @property
    def couleur_progression(self):
        p = float(self.progression_calculee)
        if p >= 70:
            return 'success'
        if p >= 30:
            return 'warning'
        return 'danger'

    def recalculer_progression(self):
        """Recalcule la progression pondérée depuis les tâches."""
        from apps.tasks.models import Tache
        taches = Tache.objects.filter(projet=self)
        total_poids = sum(float(t.poids) for t in taches)
        if total_poids > 0:
            progression = sum(
                float(t.avancement) * float(t.poids)
                for t in taches
            ) / total_poids
            self.progression_calculee = round(progression, 2)
            self.save(update_fields=['progression_calculee'])


class ProjetEntite(models.Model):
    projet      = models.ForeignKey(Projet, on_delete=models.CASCADE)
    entite      = models.ForeignKey(Entite, on_delete=models.CASCADE)
    role_entite = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = [['projet', 'entite']]


class ProjetSite(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    site   = models.ForeignKey(Site, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['projet', 'site']]


class MigrationConteneurLog(models.Model):
    projet             = models.ForeignKey(Projet, on_delete=models.CASCADE)
    conteneur_source   = models.ForeignKey(
        Conteneur, on_delete=models.PROTECT, related_name='migrations_source')
    conteneur_cible    = models.ForeignKey(
        Conteneur, on_delete=models.PROTECT, related_name='migrations_cible')
    date_migration     = models.DateTimeField(auto_now_add=True)
    migre_par          = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    commentaire        = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Log Migration Conteneur'
        ordering = ['-date_migration']


class ProjetCurvePoint(models.Model):

    GRANULARITE_CHOICES = [
        ('DAY', 'Jour'),
        ('WEEK', 'Semaine'),
        ('MONTH', 'Mois'),
        ('QUARTER', 'Trimestre'),
        ('SEMESTER', 'Semestre'),
        ('YEAR', 'Année'),
    ]

    projet = models.ForeignKey(
        Projet,
        on_delete=models.CASCADE,
        related_name="curve_points"
    )

    date = models.DateField()

    granularite = models.CharField(
        max_length=20,
        choices=GRANULARITE_CHOICES,
        default='MONTH'
    )

    planned_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    earned_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    actual_cost = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    forecast_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )


    class Meta:

        ordering = ['date']

        unique_together = [
            ['projet', 'date', 'granularite']
        ]


    def __str__(self):

        return f"{self.projet.code} - {self.date}"



class ForecastRule(models.Model):

    METHODES = [

        ('CPI',
         'EAC basé sur CPI'),

        ('SPI',
         'Projection planning'),

        ('HYBRID',
         'Modèle hybride'),

    ]


    projet = models.OneToOneField(
        Projet,
        on_delete=models.CASCADE,
        related_name="forecast_rule"
    )


    methode = models.CharField(
        max_length=20,
        choices=METHODES,
        default='CPI'
    )


    poids_cout = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=50
    )


    poids_planning = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=50
    )


    mise_a_jour_auto = models.BooleanField(
        default=True
    )


    date_derniere_calcul = models.DateTimeField(
        null=True,
        blank=True
    )