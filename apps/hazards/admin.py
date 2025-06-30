from django.contrib import admin, messages
from django.contrib.gis.admin import GISModelAdmin
from django.utils.translation import ngettext

from import_export.admin import ImportExportModelAdmin

from .models import ExposureCoverage, Hazard, HazardExposure, UrbanizationDegree
from .tasks import update_exposure_coverage_raster


@admin.register(Hazard)
class HazardAdmin(ImportExportModelAdmin):
    list_display = ["name", "code", "uuid", "id"]
    list_display_links = ["name", "code"]
    prepopulated_fields = {"code": ["name"]}
    search_fields = ["id", "uuid", "name", "code"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]


@admin.register(UrbanizationDegree)
class UrbanizationDegreeAdmin(ImportExportModelAdmin):
    list_display = ["name", "code", "uuid", "id"]
    list_display_links = ["name", "code"]
    prepopulated_fields = {"code": ["name"]}
    search_fields = ["id", "uuid", "name", "code"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]


@admin.register(ExposureCoverage)
class ExposureCoverageAdmin(GISModelAdmin, ImportExportModelAdmin):
    list_display = [
        "administrative_area__name",
        "administrative_area__country",
    ]
    list_display_links = ["administrative_area__name"]
    list_select_related = ["administrative_area"]
    list_filter = ["administrative_area__country", "created_at", "updated_at"]
    raw_id_fields = ["administrative_area"]
    search_fields = ["id", "uuid", "administrative_area__name"]
    readonly_fields = ["id", "uuid", "tms_url", "created_at", "updated_at"]
    actions = ["refresh_raster"]

    def get_queryset(self, request):
        return super().get_queryset(request).defer("raster")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if "refresh_raster" in actions:
                del actions["refresh_raster"]

        return actions

    @admin.action(description="Refresh selected raster data in the database")
    def refresh_raster(self, request, queryset):
        for mobile_coverage in queryset:
            update_exposure_coverage_raster.delay(pk=mobile_coverage.pk)

        count = len(queryset)
        self.message_user(
            request,
            ngettext(
                "%d exposure coverage raster will be updated in the database.",
                "%d exposure coverage rasters will be updated in the database.",
                count,
            )
            % count,
            messages.SUCCESS,
        )


@admin.register(HazardExposure)
class HazardExposureAdmin(ImportExportModelAdmin):
    list_display = [
        "display_name",
        "coverage__administrative_area__name",
        "coverage__administrative_area__country",
        "population_exposed_percent",
        "population_exposed_ev_percent",
    ]
    list_display_links = ["display_name", "coverage__administrative_area__name"]
    list_select_related = ["coverage__administrative_area"]
    list_filter = [
        "coverage__administrative_area__country",
        "hazards",
        "urbanization_degree",
        "created_at",
        "updated_at",
    ]
    filter_horizontal = ["hazards"]
    raw_id_fields = ["coverage"]
    search_fields = ["id", "uuid", "coverage__administrative_area__name"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("hazards").defer("coverage__raster")
