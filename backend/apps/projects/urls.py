from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [

    # LISTE & DETAILS
    path('',                    views.projet_list,          name='list'),
    path('<int:pk>/',           views.projet_detail,        name='detail'),

    # CREATE & MODIF
    path('nouveau/',            views.projet_create,        name='create'),
    path('<int:pk>/modifier/',  views.projet_edit,          name='edit'),

    # MIGRATIONS & SUPPRESSIONS /MIGRATIONS
    path('<int:pk>/supprimer/', views.projet_migrate,       name='supprimer'),
    path('<int:pk>/migrer/',    views.projet_migrate,       name='migrate'),
    path('corbeille/',          views.projet_trash,         name='trash'),

    # S-CURVE
    path('<int:pk>/scurve/',        views.projet_scurve,        name='scurve'),

]