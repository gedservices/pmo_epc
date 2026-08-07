from django.db import models


class Pays(models.Model):
    code_pays = models.CharField(max_length=5, unique=True)
    nom       = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Pays'
        verbose_name_plural = 'Pays'
        ordering = ['nom']

    def __str__(self):
        return f"{self.code_pays} — {self.nom}"


class Site(models.Model):
    code_site = models.CharField(max_length=10, unique=True)
    nom       = models.CharField(max_length=100)
    pays      = models.ForeignKey(Pays, on_delete=models.PROTECT,
                                  related_name='sites')
    actif     = models.BooleanField(default=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return f"{self.code_site} — {self.nom}"


class Secteur(models.Model):
    code_secteur = models.CharField(max_length=10, unique=True)
    nom          = models.CharField(max_length=100)
    site         = models.ForeignKey(Site, on_delete=models.PROTECT,
                                     related_name='secteurs')
    actif        = models.BooleanField(default=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return f"{self.code_secteur} — {self.nom}"


class Systeme(models.Model):
    code_systeme = models.CharField(max_length=20, unique=True)
    nom          = models.CharField(max_length=100)
    secteur      = models.ForeignKey(Secteur, on_delete=models.PROTECT,
                                     related_name='systemes')
    actif        = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Système'
        ordering = ['nom']

    def __str__(self):
        return f"{self.code_systeme} — {self.nom}"


class SousSysteme(models.Model):
    code_sous_systeme = models.CharField(max_length=20, unique=True)
    nom               = models.CharField(max_length=100)
    systeme           = models.ForeignKey(Systeme, on_delete=models.PROTECT,
                                          related_name='sous_systemes')
    actif             = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Sous-Système'
        ordering = ['nom']

    def __str__(self):
        return f"{self.code_sous_systeme} — {self.nom}"


class Discipline(models.Model):
    code  = models.CharField(max_length=10, unique=True)
    nom   = models.CharField(max_length=100)
    actif = models.BooleanField(default=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} — {self.nom}"


class Tag(models.Model):
    code_tag       = models.CharField(max_length=50, unique=True)
    description    = models.TextField(blank=True)
    type_equipement = models.CharField(max_length=100, blank=True)
    discipline     = models.ForeignKey(Discipline, on_delete=models.SET_NULL,
                                       null=True, blank=True)
    sous_systeme   = models.ForeignKey(SousSysteme, on_delete=models.SET_NULL,
                                       null=True, blank=True)
    actif          = models.BooleanField(default=True)

    class Meta:
        ordering = ['code_tag']

    def __str__(self):
        return self.code_tag


class Phase(models.Model):
    code  = models.CharField(max_length=10, unique=True)
    nom   = models.CharField(max_length=100)
    ordre = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return f"{self.code} — {self.nom}"


class ClasseDocumentaire(models.Model):
    numero          = models.IntegerField(unique=True)
    libelle         = models.CharField(max_length=50)
    description     = models.TextField(blank=True)
    cycle_simplifie = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Classe Documentaire'
        ordering = ['numero']

    def __str__(self):
        return f"Classe {self.numero} — {self.libelle}"


class StatutCycleVie(models.Model):
    code         = models.CharField(max_length=10, unique=True)
    libelle      = models.CharField(max_length=100)
    description  = models.TextField(blank=True)
    est_terminal = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Statut Cycle de Vie'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} — {self.libelle}"


class SequenceStatut(models.Model):
    phase           = models.ForeignKey(Phase, on_delete=models.CASCADE)
    classe_num      = models.IntegerField()
    statut          = models.ForeignKey(StatutCycleVie, on_delete=models.CASCADE)
    ordre           = models.IntegerField()
    est_statut_final = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Séquence de Statut'
        unique_together = [['phase', 'classe_num', 'ordre']]
        ordering = ['phase', 'classe_num', 'ordre']

    def __str__(self):
        return (f"Phase {self.phase.code} / Cl.{self.classe_num} "
                f"/ Ordre {self.ordre} → {self.statut.code}")


class DocTypeTechnique(models.Model):
    code       = models.CharField(max_length=20, unique=True)
    libelle    = models.CharField(max_length=100)
    classe_num = models.IntegerField(null=True, blank=True)
    discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL,
                                   null=True, blank=True)
    actif      = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Type de Document Technique'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} — {self.libelle}"


class DocTypeCorrespondance(models.Model):
    code    = models.CharField(max_length=20, unique=True)
    libelle = models.CharField(max_length=100)
    actif   = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Type de Document Correspondance'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} — {self.libelle}"


class Conteneur(models.Model):
    code        = models.CharField(max_length=20, unique=True)
    libelle     = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ordre       = models.IntegerField(default=0)
    est_archive = models.BooleanField(default=False)
    actif       = models.BooleanField(default=True)

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return self.libelle