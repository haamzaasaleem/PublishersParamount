from django.contrib import admin

from manuscripts.models import Manuscript,Figure,ManuRev

# Register your models here.
admin.site.register(Manuscript)
admin.site.register(Figure)
admin.site.register(ManuRev)
