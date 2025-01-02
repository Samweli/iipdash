"""
Educational Institution admin configurations.

This module defines the admin interface for the
:class:`education.models.Category`, :class:`education.models.Ownership`
and :class:`education.models.Institution` models.

References:
    - :class:`education.models.Category`
    - :class:`education.models.Ownership`
    - :class:`education.models.Institution`
    - :class:`django.contrib.gis.admin.GISModelAdmin`
    - :class:`import_export.admin.ImportExportModelAdmin`
"""

from django.contrib.gis import admin
from django.contrib.gis.admin import GISModelAdmin

from import_export.admin import ImportExportModelAdmin

from .models import Category, Institution, Ownership


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    """
    Admin interface configuration for the :class:`education.models.Category` model.

    This class extends :class:`import_export.admin.ImportExportModelAdmin` for
    data import and export.
    """

    #: A list of fields to display in the admin change list view
    list_display: list[str] = ["name", "code", "description", "id", "uuid"]

    #: A list of fields in the admin's list view that link to the detailed
    #: area editing page.
    list_display_links: list[str] = ["name", "id", "uuid"]

    #: A list of fields that can be searched in the admin interface.
    search_fields: list[str] = ["name", "code", "id", "uuid"]

    #: A list of fields that are displayed as read-only in the admin interface.
    readonly_fields: list[str] = ["id", "uuid", "created_at", "updated_at"]


@admin.register(Ownership)
class OwnershipAdmin(ImportExportModelAdmin):
    """
    Admin interface configuration for the :class:`education.models.Ownership` model.

    This class extends :class:`import_export.admin.ImportExportModelAdmin` for
    data import and export.
    """

    #: A list of fields to display in the admin change list view
    list_display: list[str] = ["name", "code", "description", "id", "uuid"]

    #: A list of fields in the admin's list view that link to the detailed
    #: area editing page.
    list_display_links: list[str] = ["name", "id", "uuid"]

    #: A list of fields that can be searched in the admin interface.
    search_fields: list[str] = ["name", "code", "id", "uuid"]

    #: A list of fields that are displayed as read-only in the admin interface.
    readonly_fields: list[str] = ["id", "uuid", "created_at", "updated_at"]


@admin.register(Institution)
class InstitutionAdmin(GISModelAdmin, ImportExportModelAdmin):
    """
    Admin interface configuration for the :class:`education.models.Institution` model.

    This class extends :class:`django.contrib.gis.admin.GISModelAdmin`
    for managing geographic data, and
    :class:`import_export.admin.ImportExportModelAdmin` for data import and
    export.
    """

    #: A list of fields to display in the admin change list view
    list_display: list[str] = [
        "name",
        "category",
        "ownership",
        "administrative_area__country",
        "administrative_area__name",
        "id",
        "uuid",
    ]

    #: A list of fields in the admin's list view that link to the detailed
    #: area editing page.
    list_display_links: list[str] = ["name", "id", "uuid"]

    #: A list of fields for filtering results in the admin change list view.
    list_filter: list[str] = ["category", "ownership", "administrative_area__country"]

    #: A list of fields that can be searched in the admin interface.
    search_fields: list[str] = ["name", "code", "id", "uuid"]

    #: A list of fields that are displayed as read-only in the admin interface.
    readonly_fields: list[str] = ["id", "uuid", "created_at", "updated_at"]
