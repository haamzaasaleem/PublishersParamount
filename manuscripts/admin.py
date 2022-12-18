from django.contrib import admin

from manuscripts.models import Manuscript, Figure, ManuRev, ManuEditor, CoAuthorModels

# Register your models here.
admin.site.register(Manuscript)
admin.site.register(Figure)
admin.site.register(ManuRev)
admin.site.register(ManuEditor)
admin.site.register(CoAuthorModels)
