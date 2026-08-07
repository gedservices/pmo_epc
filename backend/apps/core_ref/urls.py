from django.urls import path
from . import views

app_name = 'core_ref'

urlpatterns = [
    path('', views.index, name='index'),
    path('conteneur/<int:pk>/activer/', views.set_conteneur, name='set_conteneur'),
]