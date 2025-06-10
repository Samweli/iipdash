"""
Infrastructure admin configurations.

This module defines the admin interface for the
:class:`infrastructure.models.FiberOptic`,
and :class:`infrastructure.models.CellTower` models.

References:
    - :class:`infrastructure.models.FiberOptic`
    - :class:`infrastructure.models.CellTower`
    - :class:`django.contrib.gis.admin.GISModelAdmin`
    - :class:`import_export.admin.ImportExportModelAdmin`
"""

from django.contrib import admin, messages
from django.contrib.gis.admin import GISModelAdmin
from django.utils.translation import ngettext

from import_export.admin import ImportExportModelAdmin

from .models import (
    CellTower,
    ElectricityNetwork,
    FiberOptic,
    FiberOpticNode,
    InternetSpeed,
    MobileCoverage,
    NetworkGeneration,
)
from .tasks import generate_mobile_coverage_tiles, update_mobile_coverage_raster


@admin.register(FiberOptic)
class FiberOpticAdmin(GISModelAdmin, ImportExportModelAdmin):
    """
    Admin interface configuration for the
    :class:`infrastructure.models.FiberOptic` model.

    This class extends :class:`django.contrib.gis.admin.GISModelAdmin`
    for managing geographic data, and
    :class:`import_export.admin.ImportExportModelAdmin` for data import and
    export.
    """

    list_display = ["display_name", "administrative_area__country", "administrative_area", "status"]

    list_select_related = ["administrative_area"]

    #: A list of fields for filtering results in the admin change list view.
    list_filter = ["administrative_area__country", "status", "created_at", "updated_at"]

    #: A list of fields that can be searched in the admin interface.
    search_fields = ["operator_name", "name", "administrative_area__name", "id", "uuid"]

    raw_id_fields = ["administrative_area"]

    #: A list of fields that are displayed as read-only in the admin interface.
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]


@admin.register(FiberOpticNode)
class FiberOpticNodeAdmin(GISModelAdmin, ImportExportModelAdmin):

    list_filter = [
        "node_type",
        "administrative_area__country",
        "created_at",
        "updated_at",
    ]
    list_select_related = ["administrative_area"]
    raw_id_fields = ["administrative_area"]
    search_fields = ["id", "uuid", "administrative_area__name"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]


@admin.register(NetworkGeneration)
class NetworkGenerationAdmin(ImportExportModelAdmin):
    prepopulated_fields = {"code": ["name"]}
    search_fields = ["id", "uuid", "name", "code"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]


@admin.register(CellTower)
class CellTowerAdmin(GISModelAdmin, ImportExportModelAdmin):
    """
    Admin interface configuration for the
    :class:`infrastructure.models.CellTower` model.

    This class extends :class:`django.contrib.gis.admin.GISModelAdmin`
    for managing geographic data, and
    :class:`import_export.admin.ImportExportModelAdmin` for data import and
    export.
    """

    #: A list of fields for filtering results in the admin change list view.
    list_filter = [
        "network_type",
        "administrative_area__country",
        "location_is_approximate",
        "created_at",
        "updated_at",
    ]

    #: A list of fields that can be searched in the admin interface.
    search_fields = ["id", "uuid"]

    raw_id_fields = ["administrative_area"]

    #: A list of fields that are displayed as read-only in the admin interface.
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]


@admin.register(MobileCoverage)
class MobileCoverageAdmin(GISModelAdmin, ImportExportModelAdmin):
    list_display = [
        "network_generation",
        "administrative_area",
        "administrative_area__country",
        "population_uncovered_percent",
    ]
    list_display_links = ["network_generation", "administrative_area"]
    list_select_related = ["network_generation", "administrative_area"]
    list_filter = ["network_generation", "administrative_area__country", "created_at", "updated_at"]
    raw_id_fields = ["administrative_area"]
    search_fields = ["id", "uuid", "administrative_area__name"]
    readonly_fields = ["id", "uuid", "tms_url", "created_at", "updated_at"]
    actions = ["refresh_raster", "refresh_tiles"]

    @admin.action(description="Refresh selected raster data in the database")
    def refresh_raster(self, request, queryset):
        for mobile_coverage in queryset:
            update_mobile_coverage_raster.delay(pk=mobile_coverage.pk)

        count = len(queryset)
        self.message_user(
            request,
            ngettext(
                "%d mobile coverage raster will be updated in the database.",
                "%d mobile coverage rasters will be updated in the database.",
                count,
            )
            % count,
            messages.SUCCESS,
        )

    @admin.action(description="Regenerate selected mobile coverage TMS tiles")
    def refresh_tiles(self, request, queryset):
        for mobile_coverage in queryset:
            generate_mobile_coverage_tiles.delay(pk=mobile_coverage.pk)

        count = len(queryset)
        self.message_user(
            request,
            ngettext(
                "%d mobile coverage tile set is going to be updated.",
                "%d mobile coverage tiles sets are going to be updated.",
                count,
            )
            % count,
            messages.SUCCESS,
        )


@admin.register(ElectricityNetwork)
class ElectricityNetworkAdmin(GISModelAdmin, ImportExportModelAdmin):
    list_display = ["display_name", "administrative_area", "status", "network_type"]
    list_display_links = ["display_name", "administrative_area"]
    list_filter = ["administrative_area__country", "created_at", "updated_at"]
    list_select_related = ["administrative_area"]
    search_fields = ["id", "uuid", "administrative_area__name"]
    raw_id_fields = ["administrative_area"]


@admin.register(InternetSpeed)
class InternetSpeedAdmin(ImportExportModelAdmin):
    pass
