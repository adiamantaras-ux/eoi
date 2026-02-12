# organizations/admin.py
from django.contrib import admin
from .models import Region, Club


@admin.action(description="✅ Ενεργοποίηση")
def make_active(modeladmin, request, queryset):
    if hasattr(modeladmin.model, "is_active"):
        queryset.update(is_active=True)


@admin.action(description="⛔ Απενεργοποίηση")
def make_inactive(modeladmin, request, queryset):
    if hasattr(modeladmin.model, "is_active"):
        queryset.update(is_active=False)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)
    actions = (make_active, make_inactive)


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "region", "email", "phone", "is_active")
    list_filter = ("is_active", "region")
    search_fields = ("code", "name", "email", "phone", "region__name")
    ordering = ("code",)
    actions = (make_active, make_inactive)

    # ✅ Autocomplete περιφέρειας
    autocomplete_fields = ("region",)
