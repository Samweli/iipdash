from django.contrib.gis import admin

from import_export.admin import ImportExportModelAdmin

from .models import Category, Layer


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ["name", "description", "uuid", "id"]
    list_display_links = ["name", "id", "uuid"]
    search_fields = ["name", "id", "uuid"]
    prepopulated_fields = {"code": ["name"]}
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]


@admin.register(Layer)
class LayerAdmin(ImportExportModelAdmin):
    list_display = ["name", "uuid", "id"]
    list_display_links = ["name", "id", "uuid"]
    list_filter = ["categories", "created_at", "updated_at"]
    search_fields = ["name", "tags", "source"]
    filter_horizontal = ["categories"]
    prepopulated_fields = {"code": ["name"]}
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]
