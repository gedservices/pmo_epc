"""
Django settings for core project.
Refactor Phase 0 — env via python-decouple, pas de secrets en dur.
"""
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="django-insecure-change-me")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

# =============================================================
# APPLICATIONS
# =============================================================
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'django_filters',
    'django_tables2',
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
    'guardian',
]

LOCAL_APPS = [
    'apps.planning',          # Suivi opérationnel des tâches (vue analytique, sans modèle propre)
    'apps.planning_project',  # Moteur planning projet (baselines, dépendances, chemin critique)
    'apps.accounts',
    'apps.contracts',
    'apps.core_ref',
    'apps.costs',
    'apps.dashboard',
    'apps.documents',         # GED / cycle de vie documentaire — référencé par tâches/commandes/projets
    'apps.projects',
    'apps.reporting',
    'apps.risks',
    'apps.tasks',
    'apps.workflows',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
                "apps.core_ref.context_processors.global_context",
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

# =============================================================
# DATABASE — via .env (port 5433 historique)
# =============================================================
DATABASES = {
    'default': {
        'ENGINE': config("DB_ENGINE", default="django.db.backends.postgresql"),
        'NAME': config("DB_NAME", default="pmo_epc_db"),
        'USER': config("DB_USER", default="postgres"),
        'PASSWORD': config("DB_PASSWORD", default="openpgpwd"),
        'HOST': config("DB_HOST", default="localhost"),
        'PORT': config("DB_PORT", default="5433"),
    }
}

LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/auth/login/'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
]
AUTH_USER_MODEL = "accounts.User"

# =============================================================
# I18N
# =============================================================
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Libreville'
USE_I18N = True
USE_TZ = True

# =============================================================
# STATIC / MEDIA
# =============================================================
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# =============================================================
# MESSAGES
# =============================================================
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

DEFAULT_PAGE_SIZE = 25

# =============================================================
# PMO CONFIG
# =============================================================
PMO_CONFIG = {
    'APP_NAME': 'PMO EPC Platform',
    'APP_VERSION': '1.0.0',
    'COMPANY_NAME': 'GED-SERVICES',
    'DEFAULT_REVIEW_DURATION_COMPANY': 15,
    'DEFAULT_REVIEW_DURATION_CONTRACTOR': 15,
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "file": {"class": "logging.FileHandler", "filename": str(LOG_DIR / "pmo_epc.log")},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}

APPS_DIR = BASE_DIR / "apps"
