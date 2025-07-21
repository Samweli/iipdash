from django.db.models import Q

from django_filters import rest_framework as filters

from hazards.models import HazardExposure

from ..models import Area

__all__ = ["AreaFilter", "AreaHazardExposureFilter"]


class AreaFilter(filters.FilterSet):
    level = filters.NumberFilter(field_name="depth")

    class Meta:
        model = Area
        fields = ["uuid", "level", "country"]


class AreaHazardExposureFilter(filters.FilterSet):

    uuid = filters.UUIDFilter(field_name="administrative_area_uuid")
    country = filters.CharFilter(field_name="country")
    level = filters.NumberFilter(field_name="depth")
    hazard_code_in = filters.BaseCSVFilter(method="noop")
    urbanization_degree_code_in = filters.BaseCSVFilter(method="noop")
    urbanization_degree_group = filters.CharFilter(method="noop")

    class Meta:
        model = HazardExposure
        fields = ["uuid", "country", "level", "hazard_code_in", "urbanization_degree_code_in"]

    def noop(self, queryset, *args, **kwargs):
        """Return the queryset as is.

        Used here to allow explicit handling the filtering outside filter set context
        """
        return queryset

    def get_aggregates_filter(self) -> Q:
        """Returns Q object for filtering aggerations."""
        q_filters = Q()

        if self.is_valid():

            # hazards
            hazard_code_in = self.form.cleaned_data.get("hazard_code_in")
            if hazard_code_in:
                # hazards matching any of the codes
                q_filters &= Q(hazards_codes__overlap=hazard_code_in)
            else:
                # don't include exposures with no hazards
                q_filters &= ~Q(hazards_codes=[])

            # urbanization degrees
            urbanization_degree_code_in = self.form.cleaned_data.get("urbanization_degree_code_in")
            if urbanization_degree_code_in:
                q_filters &= Q(urbanization_degree__code__in=urbanization_degree_code_in)

            # urbanization degree group
            urbanization_degree_group = self.form.cleaned_data.get("urbanization_degree_group")
            if urbanization_degree_group:
                q_filters &= Q(urbanization_degree__group=urbanization_degree_group)

        return q_filters
