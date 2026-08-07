"""
URL configuration for core — Phase 0 : fix double include planning.
- planning/            -> apps.planning (suivi opérationnel des tâches)
- planning-projet/     -> apps.planning_project (moteur planning projet / baselines)
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Suivi opérationnel : vue analytique sur Tâches (Gantt, retards, jalons, charge) — sans modèle propre
    path("planning/", include("apps.planning.urls", namespace='planning')),
    # Moteur planning projet : baselines, versions, dépendances, chemin critique
    path("planning-projet/", include("apps.planning_project.urls", namespace='planning_project')),
    path("documents/", include("apps.documents.urls", namespace='documents')),
    path('auth/', include('apps.accounts.urls', namespace='accounts')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    path('projects/', include('apps.projects.urls', namespace='projects')),
    path('contracts/', include('apps.contracts.urls', namespace='contracts')),
    path('tasks/', include('apps.tasks.urls', namespace='tasks')),
    path('costs/', include('apps.costs.urls', namespace='costs')),
    path('risks/', include('apps.risks.urls', namespace='risks')),
    path('reporting/', include('apps.reporting.urls', namespace='reporting')),
    path('referentiels/', include('apps.core_ref.urls', namespace='core_ref')),
    path('', include('apps.dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
