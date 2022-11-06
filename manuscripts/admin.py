from django.contrib import admin

from manuscripts.models import Manuscript,Figure

# Register your models here.
admin.site.register(Manuscript)
admin.site.register(Figure)