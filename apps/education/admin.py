from django.contrib.gis import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import Category, Institution, Ownership


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "description", "id", "uuid"]
    list_display_links = ["name", "id", "uuid"]
    search_fields = ["name", "code", "id", "uuid"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "description", "id", "uuid"]
    list_display_links = ["name", "id", "uuid"]
    search_fields = ["name", "code", "id", "uuid"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]


@admin.register(Institution)
class InstitutionAdmin(GISModelAdmin):
    list_display = [
        "name",
        "category",
        "ownership",
        "administrative_area__country",
        "administrative_area__name",
        "id",
        "uuid",
    ]
    list_display_links = ["name", "id", "uuid"]
    list_filter = ["category", "ownership", "administrative_area__country"]
    search_fields = ["name", "code", "id", "uuid"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]
