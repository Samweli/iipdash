from django_filters import rest_framework as filters

from hazards.models import HazardExposure

from ..models import Area

__all__ = ["AreaFilter", "AreaHazardExposureFilter", "AreaHazardExposureFilter2"]


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

    hazard_type = CommaSeparatedCharFilter(
        field_name="hazards_exposure_coverage__exposure__hazards__code", lookup_expr="in"
    )
    urbanization_degree = CommaSeparatedCharFilter(
        field_name="hazards_exposure_coverage__exposure__urbanization_degree__code", lookup_expr="in"
    )

    class Meta:
        model = Area
        fields = ["administrative_area", "administrative_area_level", "hazard_type", "urbanization_degree"]


class AreaHazardExposureFilter2(filters.FilterSet):

    administrative_area = filters.UUIDFilter(field_name="administrative_area_uuid")
    administrative_area_level = filters.NumberFilter(field_name="administrative_area_depth")
    hazard_type_code = filters.BaseInFilter(field_name="hazards__code")
    urbanization_degree_code = filters.BaseInFilter(field_name="urbanization_degree__code")

    class Meta:
        model = HazardExposure
        fields = ["administrative_area", "administrative_area_level", "hazard_type_code", "urbanization_degree_code"]
