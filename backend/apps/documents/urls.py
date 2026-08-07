from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    # DASHBOARD
    path('', views.dashboard, name='dashboard'),

    # LISTE
    path('liste/', views.document_list, name='list'),

    # ⭐ NOUVEAU : Cycle de vie
    path('lifecycle/', views.document_lifecycle, name='lifecycle'),

    # ⭐ NOUVEAU : Vue par état
    path('status/', views.document_status_view, name='status'),

    # CRUD DOCUMENT
    path('nouveau/', views.document_create, name='create'),
    path('<int:pk>/', views.document_detail, name='detail'),
    # path('<int:pk>/modifier/', views.document_edit, name='edit'),
    # path('<int:pk>/supprimer/', views.document_delete, name='delete'),
    # path('<int:pk>/historique/', views.document_history, name='history'),

    # RÉVISIONS (futures)
    # path('<int:doc_pk>/nouvelle-revision/', views.revision_create, name='revision_create'),
    # path('revision/<int:pk>/retour/', views.revision_retour, name='revision_retour'),
    # path('revision/<int:pk>/telecharger/', views.document_download, name='download'),
    # path('revision/<int:pk>/viewer/', views.document_viewer, name='viewer'),

    # TRANSMITTALS (futures)
    # path('transmittals/', views.transmittal_list, name='transmittals'),
]