from django.urls import path
from . import views

app_name = "planning_project"

urlpatterns = [

    path("", views.dashboard, name="dashboard"),

    path("planning/", views.planning, name="planning"),

    path("versions/", views.versions, name="versions"),
    path("baseline/", views.baseline, name="baseline"),

    path("dependencies/", views.dependencies, name="dependencies"),
    path("constraints/", views.constraints, name="constraints"),

    path("resources/", views.resources, name="resources"),
    path("calendars/", views.calendars, name="calendars"),

    path("critical-path/", views.critical_path, name="critical_path"),

    path("api/gantt/", views.gantt_data, name="gantt_data"),
]