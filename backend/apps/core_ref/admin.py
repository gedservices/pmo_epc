from django.contrib import admin

# Register your models here.

from django.contrib import admin
# from django.template.backends.jinja2 import Origin

from .models import (Pays, Site, Secteur, Systeme, SousSysteme,
                     Discipline, Tag, Phase, ClasseDocumentaire,
                     StatutCycleVie, SequenceStatut, DocTypeTechnique,
                     DocTypeCorrespondance, Conteneur, Originator)

admin.site.register(Pays)
admin.site.register(Site)
admin.site.register(Secteur)
admin.site.register(Systeme)
admin.site.register(SousSysteme)
admin.site.register(Discipline)
admin.site.register(Tag)
admin.site.register(Phase)
admin.site.register(ClasseDocumentaire)
admin.site.register(StatutCycleVie)
admin.site.register(SequenceStatut)
admin.site.register(DocTypeTechnique)
admin.site.register(DocTypeCorrespondance)
admin.site.register(Conteneur)
admin.site.register(Originator)
