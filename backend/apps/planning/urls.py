from django.urls import path
from . import views

app_name = "planning"

urlpatterns = [

    path("", views.dashboard, name="dashboard"),

    path("projets/", views.par_projet, name="projets"),

    path("commandes/", views.par_commande, name="commandes"),

    path("responsables/", views.par_responsable, name="responsables"),

    path("gantt/", views.gantt, name="gantt"),

    path("calendrier/", views.calendrier, name="calendrier"),

    path("retards/", views.retards, name="retards"),

    path("jalons/", views.jalons, name="jalons"),

    path("charge/", views.charge, name="charge"),
]