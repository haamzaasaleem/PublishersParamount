from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import *


    
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "role", "gender")
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {"fields": (
            "is_active",
            "is_staff",
            "is_superuser",
        ), }),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', "role", "gender", "user_image",),
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Author)
admin.site.register(Editor)
admin.site.register(EditorInChief)
admin.site.register(Reviewer)
admin.site.register(EicStaff)
admin.site.register(EditorStaff)
