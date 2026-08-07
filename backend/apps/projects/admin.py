from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Projet, ProjetEntite, ProjetSite, MigrationConteneurLog


class ProjetEntiteInline(admin.TabularInline):
    model = ProjetEntite
    extra = 1


class ProjetSiteInline(admin.TabularInline):
    model = ProjetSite
    extra = 1


@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display  = ['code', 'nom', 'statut', 'priorite',
                     'progression_calculee', 'conteneur', 'responsable']
    list_filter   = ['statut', 'priorite', 'conteneur', 'type_projet']
    search_fields = ['code', 'nom']
    inlines       = [ProjetEntiteInline, ProjetSiteInline]
