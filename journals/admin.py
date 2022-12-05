from django.contrib import admin

from journals.models import *

# Register your models here.
admin.site.register(Journal)
admin.site.register(Subject)