from django_filters import rest_framework as filters

from ..models import Area

__all__ = ["AreaFilter"]


class AreaFilter(filters.FilterSet):
    level = filters.NumberFilter(field_name="depth")

    class Meta:
        model = Area
        fields = ["uuid", "level", "country"]
