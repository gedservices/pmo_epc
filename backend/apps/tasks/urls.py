from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('',                   views.tache_list,   name='list'),
    path('<int:pk>/',          views.tache_detail, name='detail'),
    path('nouveau/',           views.tache_create, name='create'),
    path('<int:pk>/modifier/', views.tache_edit,   name='edit'),
    path('<int:pk>/supprimer/',views.tache_delete, name='delete'),
    path('gantt/',             views.gantt,         name='gantt'),
    path('api/gantt-data/',    views.gantt_data,    name='gantt_data'),
]