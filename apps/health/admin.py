from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from import_export.admin import ImportExportModelAdmin

from .models import HealthFacility


@admin.register(HealthFacility)
class HealthFacilityAdmin(GISModelAdmin, ImportExportModelAdmin):
    pass
