from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from import_export.admin import ImportExportModelAdmin

from .models import ExposureCoverage, Hazard, HazardExposure


@admin.register(Hazard)
class HazardAdmin(ImportExportModelAdmin):
    list_display = ["name", "code", "uuid", "id"]
    list_display_links = ["name", "code"]
    prepopulated_fields = {"code": ["name"]}
    search_fields = ["id", "uuid", "name", "code"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]


@admin.register(ExposureCoverage)
class ExposureCoverageAdmin(GISModelAdmin, ImportExportModelAdmin):
    list_display = [
        "display_name",
        "administrative_area__country",
    ]
    list_display_links = ["display_name"]
    list_select_related = ["administrative_area"]
    list_filter = ["administrative_area__country", "created_at", "updated_at"]
    raw_id_fields = ["administrative_area"]
    search_fields = ["id", "uuid", "administrative_area__name"]
    readonly_fields = ["id", "uuid", "tms_url", "created_at", "updated_at"]


@admin.register(HazardExposure)
class HazardExposureAdmin(ImportExportModelAdmin):
    list_display = [
        "display_name",
        "coverage__administrative_area__country",
        "population_exposed_percent",
        "population_exposed_ev_percent",
    ]
    list_display_links = ["display_name"]
    list_select_related = ["coverage__administrative_area"]
    list_filter = ["coverage__administrative_area__country", "hazards", "created_at", "updated_at"]
    filter_horizontal = ["hazards"]
    raw_id_fields = ["coverage"]
    search_fields = ["id", "uuid", "coverage__administrative_area__name"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("hazards")
