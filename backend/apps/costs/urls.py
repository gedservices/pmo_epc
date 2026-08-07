from django.urls import path
from . import views
app_name = 'costs'
urlpatterns = [
    path('', views.cout_list, name='list'),
]