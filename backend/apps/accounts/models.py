

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models



from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse e-mail est obligatoire.")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)




class Entite(models.Model):
    TYPE_CHOICES = [('INTERNE', 'Interne'), ('EXTERNE', 'Externe')]
    nom         = models.CharField(max_length=100, unique=True)
    type        = models.CharField(max_length=20, choices=TYPE_CHOICES, default='INTERNE')
    description = models.TextField(blank=True)
    actif       = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Entité'
        ordering = ['type', 'nom']

    def __str__(self):
        return f"{self.nom} ({self.type})"


class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN',               'Administrateur'),
        ('PMO',                 'PMO'),
        ('MANAGER',             'Manager'),
        ('LEAD_DOC_CONTROLLER', 'Lead Doc Controller'),
        ('DOC_CONTROLLER',      'Doc Controller'),
        ('LEADER_TECHNIQUE',    'Leader Technique'),
        ('SPECIALIST',          'Spécialiste'),
        ('MEMBER',              'Membre'),
        ('CONTRACTOR',          'Contractor'),
    ]

    email           = models.EmailField(unique=True)
    entite          = models.ForeignKey(
                        Entite, on_delete=models.SET_NULL,
                        null=True, blank=True,
                        related_name='utilisateurs')
    role            = models.CharField(max_length=30, choices=ROLE_CHOICES,
                                       default='MEMBER')
    est_contractor  = models.BooleanField(default=False)
    actif           = models.BooleanField(default=True)
    avatar          = models.ImageField(upload_to='avatars/',
                                        null=True, blank=True)
    date_modification = models.DateTimeField(auto_now=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    objects = UserManager()


    class Meta:
        verbose_name = 'Utilisateur'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.role})"

    @property
    def nom_complet(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email

    @property
    def initiales(self):
        parts = [self.first_name, self.last_name]
        return ''.join(p[0].upper() for p in parts if p)

    # Helpers rôles
    @property
    def is_admin(self):
        return self.role == 'ADMIN'

    @property
    def is_pmo(self):
        return self.role in ('ADMIN', 'PMO')

    @property
    def is_doc_controller(self):
        return self.role in ('ADMIN', 'PMO', 'LEAD_DOC_CONTROLLER',
                             'DOC_CONTROLLER')

    @property
    def is_contractor_user(self):
        return self.role == 'CONTRACTOR'