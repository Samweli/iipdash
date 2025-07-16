from django_filters import rest_framework as filters

from ..models import Area

__all__ = ["AreaFilter", "AreaHazardExposureFilter"]


class AreaFilter(filters.FilterSet):
    level = filters.NumberFilter(field_name="depth")

    class Meta:
        model = Area
        fields = ["uuid", "level", "country"]


class CommaSeparatedCharFilter(filters.BaseCSVFilter, filters.CharFilter):
    pass


class AreaHazardExposureFilter(filters.FilterSet):

    administrative_area = filters.UUIDFilter(field_name="uuid")
    administrative_area_level = filters.NumberFilter(field_name="depth")

    class Meta:
        model = Area
        fields = ["administrative_area", "administrative_area_level"]
