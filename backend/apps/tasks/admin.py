from django.contrib import admin
from .models import Tache, TacheLien, TacheDocument, HistoriqueTache


class TacheDocumentInline(admin.TabularInline):
    model = TacheDocument
    extra = 0


class TacheLienInline(admin.TabularInline):
    model = TacheLien
    fk_name = "tache_source"
    extra = 0


@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ["nom", "projet", "commande", "parent", "niveau", "statut", "avancement", "poids", "est_jalon", "est_visible_planning_projet"]
    list_filter = ["statut", "niveau", "est_jalon", "phase", "discipline"]
    search_fields = ["nom", "description"]
    inlines = [TacheDocumentInline, TacheLienInline]
    readonly_fields = ["niveau", "est_en_retard", "date_creation", "date_modification"]


@admin.register(TacheLien)
class TacheLienAdmin(admin.ModelAdmin):
    list_display = ["tache_source", "tache_cible", "type_lien", "decalage_jours"]
    list_filter = ["type_lien"]
    autocomplete_fields = ["tache_source", "tache_cible"]


@admin.register(TacheDocument)
class TacheDocumentAdmin(admin.ModelAdmin):
    list_display = ["tache", "document", "role", "date_creation"]


@admin.register(HistoriqueTache)
class HistoriqueTacheAdmin(admin.ModelAdmin):
    list_display = ["tache", "champ_modifie", "date_modification", "modifie_par"]
    list_filter = ["champ_modifie"]
