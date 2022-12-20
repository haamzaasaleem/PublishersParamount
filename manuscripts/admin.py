from django.contrib import admin

from manuscripts.models import Manuscript, Figure, ManuRev, ManuEditor, CoAuthorModels

# Register your models here.

admin.site.register(Figure)

admin.site.register(CoAuthorModels)
@admin.register(Manuscript)
class ManuscriptAdmin(admin.ModelAdmin):
    list_display = ['id','title']

@admin.register(ManuRev)
class ManuRevAdmin(admin.ModelAdmin):
    list_display = ['id','manuscript']

@admin.register(ManuEditor)
class ManuEditorAdmin(admin.ModelAdmin):
    list_display = ['id','manuscript']