from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import CellTower, OpticalFibre


@admin.register(OpticalFibre)
class OpticalFibreAdmin(GISModelAdmin):
    list_filter = ["country", "created_at", "updated_at"]
    search_fields = ["id", "uuid"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]


@admin.register(CellTower)
class CellTowerAdmin(GISModelAdmin):
    list_filter = [
        "network_type",
        "administrative_area__country",
        "location_is_approximate",
        "created_at",
        "updated_at",
    ]
    search_fields = ["id", "uuid"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]
