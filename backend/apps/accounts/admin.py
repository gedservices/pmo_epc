from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Entite


@admin.register(Entite)
class EntiteAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'type', 'actif']
    list_filter   = ['type', 'actif']
    search_fields = ['nom']


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display  = ['email', 'last_name', 'first_name',
                     'role', 'entite', 'actif']
    list_filter   = ['role', 'actif', 'entite']
    search_fields = ['email', 'last_name', 'first_name']
    ordering      = ['last_name']

    fieldsets = UserAdmin.fieldsets + (
        ('PMO Info', {
            'fields': ('entite', 'role', 'est_contractor', 'actif', 'avatar')
        }),
    )
