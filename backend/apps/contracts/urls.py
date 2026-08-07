from django.urls import path
from . import views

app_name = "contracts"

urlpatterns = [

    path("", views.commande_list, name="list"),

    path("create/", views.commande_create, name="create"),

    path("<int:pk>/", views.commande_detail, name="detail"),

    path("<int:pk>/edit/", views.commande_update, name="update"),

    path("<int:pk>/delete/", views.commande_delete, name="delete"),

]