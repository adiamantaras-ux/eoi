from django.contrib import admin
from .models import Region, Club


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "region", "is_active")
    search_fields = ("code", "name")
    list_filter = ("region", "is_active")
