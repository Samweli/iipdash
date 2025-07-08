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

    administrative_area_level = filters.NumberFilter(field_name="depth")
    hazard_type = CommaSeparatedCharFilter(
        field_name="hazards_exposure_coverage__exposure__hazards__code", lookup_expr="in"
    )
    urbanization_degree = CommaSeparatedCharFilter(
        field_name="hazards_exposure_coverage__exposure__urbanization_degree__code", lookup_expr="in"
    )

    class Meta:
        model = Area
        fields = ["administrative_area_level", "hazard_type", "urbanization_degree"]
