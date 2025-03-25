from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from import_export.admin import ImportExportModelAdmin

from .models import PopulationDensityHD, RelativeWealthIndex


@admin.register(PopulationDensityHD)
class PopulationDensityHDAdmin(GISModelAdmin, ImportExportModelAdmin):
    list_display = ["administrative_area", "population_density", "id", "uuid"]
    list_display_links = ["administrative_area", "id", "uuid"]
    list_select_related = ["administrative_area"]
    raw_id_fields = ["administrative_area"]
    list_filter = ["administrative_area__country", "administrative_area", "created_at", "updated_at"]


@admin.register(RelativeWealthIndex)
class RelativeWealthIndexAdmin(GISModelAdmin, ImportExportModelAdmin):
    pass
