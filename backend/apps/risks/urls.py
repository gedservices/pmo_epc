from django.urls import path
from . import views

app_name = 'risks'

urlpatterns = [
    path('',                   views.risque_list,   name='list'),
    path('matrice/',           views.matrice,        name='matrice'),
    path('nouveau/',           views.risque_create, name='create'),
    path('<int:pk>/modifier/', views.risque_edit,   name='edit'),
    path('<int:pk>/supprimer/',views.risque_delete, name='delete'),
]