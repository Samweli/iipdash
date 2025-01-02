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

from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from import_export.admin import ImportExportModelAdmin

from .models import CellTower, FiberOptic


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

    #: A list of fields for filtering results in the admin change list view.
    list_filter = ["country", "created_at", "updated_at"]

    #: A list of fields that can be searched in the admin interface.
    search_fields = ["id", "uuid"]

    #: A list of fields that are displayed as read-only in the admin interface.
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

    #: A list of fields that are displayed as read-only in the admin interface.
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]
