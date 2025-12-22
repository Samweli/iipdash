from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from import_export.admin import ImportExportModelAdmin

from .models import HealthFacility


@admin.register(HealthFacility)
class HealthFacilityAdmin(GISModelAdmin, ImportExportModelAdmin):

    #: A list of fields to display in the admin change list view
    list_display: list[str] = [
        "name",
        "amenity",
        "administrative_area__name",
        "administrative_area__country",
        "osm_type",
        "osm_id",
        "id",
        "uuid",
    ]

    #: A list of fields in the admin's list view that link to the detailed
    #: area editing page.
    list_display_links: list[str] = ["name", "id", "uuid"]

    #: A list of fields for filtering results in the admin change list view.
    list_filter = [
        "amenity",
        "osm_type",
        "administrative_area__country",
        "created_at",
        "updated_at",
    ]

    list_select_related = ["administrative_area"]

    raw_id_fields = ["administrative_area"]

    #: A list of fields that can be searched in the admin interface.
    search_fields = ["id", "uuid", "osm_id", "name", "administrative_area__name"]

    #: A list of fields that are displayed as read-only in the admin interface.
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]
