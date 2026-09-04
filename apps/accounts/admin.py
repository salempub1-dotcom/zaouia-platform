from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class Admin(UserAdmin):
    ordering = ("email",)
    list_display = ("email", "full_name", "role", "is_active")
    fieldsets = ((None, {"fields": ("email", "password")}), ("المعلومات", {"fields": ("full_name", "role", "preferred_language")}), ("الصلاحيات", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}))
    add_fieldsets = ((None, {"fields": ("email", "full_name", "password1", "password2")}),)
