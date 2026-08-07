from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q
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

    # Rattachement principal (vérité EVM) — tombe sur Projet/Commande génériques si orphelin
    projet      = models.ForeignKey(
        'projects.Projet', on_delete=models.CASCADE,
        related_name='taches')
    commande    = models.ForeignKey(
        'contracts.Commande', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='taches')

    # Hiérarchie WBS — Option C validée : parent/niveau local, M2M projets/commandes différé Phase 2
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='enfants',
        help_text="Tâche parente (WBS). Niveau 1 = racine. 1..5 remonte en planning_project, 6..n opérationnel seul.")
    niveau = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)],
        help_text="Calculé : 1 si racine, sinon parent.niveau + 1")

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
    poids       = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                      validators=[MinValueValidator(0), MaxValueValidator(100)])
    avancement  = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                      validators=[MinValueValidator(0), MaxValueValidator(100)])

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

    # GED central : liens vers documents existants via TacheDocument (M2M explicite)
    # accesseur : tache.documents_lies.all() via related_name

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
        ordering = ['projet', 'commande', 'niveau', 'date_debut_prevue']
        constraints = [
            models.CheckConstraint(check=Q(poids__gte=0) & Q(poids__lte=100), name='tache_poids_0_100'),
            models.CheckConstraint(check=Q(avancement__gte=0) & Q(avancement__lte=100), name='tache_avancement_0_100'),
            models.CheckConstraint(check=Q(niveau__gte=1), name='tache_niveau_gte_1'),
        ]

    def __str__(self):
        return f"[N{self.niveau}] {self.nom}"

    def save(self, *args, **kwargs):
        # Niveau WBS
        if self.parent_id:
            # Empêche cycle simple
            if self.parent_id == self.pk:
                raise ValueError("Une tâche ne peut être son propre parent.")
            # parent doit être du même projet (recohérence WBS)
            parent = Tache.objects.filter(pk=self.parent_id).first()
            if parent:
                self.niveau = (parent.niveau or 1) + 1
        else:
            self.niveau = 1
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

    @property
    def est_visible_planning_projet(self):
        """Niveaux 1..5 visibles en planning_project, 6..n masqués."""
        return (self.niveau or 1) <= 5


class TacheLien(models.Model):
    """Lien peer (même niveau) entre deux tâches : dépendance FS/SS/FF/SF."""
    TYPE_CHOICES = [
        ('FS', 'Fin → Début'),
        ('SS', 'Début → Début'),
        ('FF', 'Fin → Fin'),
        ('SF', 'Début → Fin'),
    ]
    tache_source = models.ForeignKey(Tache, on_delete=models.CASCADE, related_name='liens_sortants')
    tache_cible  = models.ForeignKey(Tache, on_delete=models.CASCADE, related_name='liens_entrants')
    type_lien    = models.CharField(max_length=2, choices=TYPE_CHOICES, default='FS')
    decalage_jours = models.IntegerField(default=0, help_text="Lag positif/négatif en jours")
    cree_par     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Lien de tâche'
        unique_together = [['tache_source', 'tache_cible', 'type_lien']]
        constraints = [
            models.CheckConstraint(check=~Q(tache_source=models.F('tache_cible')), name='lien_no_self'),
        ]

    def __str__(self):
        return f"{self.tache_source_id} -{self.type_lien}({self.decalage_jours}j)-> {self.tache_cible_id}"


class TacheDocument(models.Model):
    """Lien vers un Document GED existant (source unique)."""
    tache    = models.ForeignKey(Tache, on_delete=models.CASCADE, related_name='documents_lies')
    document = models.ForeignKey('documents.Document', on_delete=models.CASCADE, related_name='taches_liees')
    role     = models.CharField(max_length=50, blank=True, help_text="Ex: référence, livrable, préalable")
    cree_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Document lié à la tâche'
        unique_together = [['tache', 'document']]

    def __str__(self):
        return f"T{self.tache_id} ↔ Doc {self.document_id}"


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
