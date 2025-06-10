from django.contrib import messages
from django.contrib.gis import admin
from django.utils.translation import ngettext

from import_export.admin import ImportExportModelAdmin

from .models import Category, Layer
from .tasks import generate_layer_tiff_tiles


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
    actions = ["refresh_tiles"]

    @admin.action(description="Regenerate TMS tiles for selected GeoTIFF layers")
    def refresh_tiles(self, request, queryset):

        tiff_count = 0
        for layer in queryset:
            if layer.tiff:
                generate_layer_tiff_tiles.delay(pk=layer.pk)
                tiff_count += 1

        count = len(queryset)

        if tiff_count:
            self.message_user(
                request,
                ngettext(
                    "%d layer tile set is going to be updated.",
                    "%d layers tiles sets are going to be updated.",
                    tiff_count,
                )
                % tiff_count,
                messages.SUCCESS,
            )
        else:
            self.message_user(
                request,
                ngettext(
                    "No GeoTIFF found in selected layer.",
                    "No GeoTIFF found in selected layers.",
                    count,
                )
                % count,
                messages.WARNING,
            )
