from django.contrib.gis import admin
from django.contrib.gis.admin import GISModelAdmin

from import_export.admin import ImportExportModelAdmin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Area


@admin.register(Area)
class AreaAdmin(TreeAdmin, GISModelAdmin, ImportExportModelAdmin):

    list_display = ["name", "type_code", "country", "id", "uuid"]
    list_display_links = ["name", "id", "uuid"]
    search_fields = ["name"]
    readonly_fields = ["id", "uuid", "full_name", "created_at", "updated_at"]
    form = movenodeform_factory(Area)
