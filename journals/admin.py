from django.contrib import admin

from journals.models import *


# Register your models here.
@admin.register(Journal)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


# admin.site.register(Subject)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
