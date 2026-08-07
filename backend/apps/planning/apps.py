# from django.apps import AppConfig
#
#
# class PlanningConfig(AppConfig):
#     # name = 'planning'
#     name = 'apps.planning'
#     verbose_name = 'Gestion de Planning'

from django.apps import AppConfig

class PlanningConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.planning"
    verbose_name = "Planning"
