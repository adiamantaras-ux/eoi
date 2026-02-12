from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    ordering = ("login_code",)
    list_display = ("login_code", "username", "email", "is_active", "is_staff", "is_superuser")
    search_fields = ("login_code", "username", "email")

    fieldsets = DjangoUserAdmin.fieldsets + (
        ("EOI", {"fields": ("login_code",)}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("EOI", {"fields": ("login_code",)}),
    )
