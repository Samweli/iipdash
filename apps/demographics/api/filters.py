from django.utils.translation import gettext_lazy as _

from django_filters import rest_framework as filters

from ..models import PopulationDensityHD

__all__ = ["PopulationDensityHDFilter"]


class PopulationDensityHDFilter(filters.FilterSet):

    country = filters.CharFilter(
        field_name="administrative_area__country",
        help_text=_("Filter by country code."),
    )

    #: Filter by multiple country codes
    country_in: filters.BaseInFilter = filters.BaseInFilter(
        field_name="administrative_area__country",
        help_text=_("Filter by multiple country codes."),
    )

    administrative_area = filters.UUIDFilter(
        field_name="administrative_area__uuid",
        help_text=_("Filter by administrative area UUID."),
    )

    #: Filter by multiple administrative area UUIDs
    administrative_area_in: filters.BaseInFilter = filters.BaseInFilter(
        field_name="administrative_area__uuid",
        help_text=_("Filter by multiple administrative area UUIDs."),
    )

    #: Filter by population density (population per ~30 square meters).
    population_density_gte = filters.NumberFilter(
        field_name="population_density",
        lookup_expr="gte",
        help_text=_("Filter by population density (population per ~30 square meters) greater than or equal i.e `>=`."),
    )

    #: Filter by distance (in meters) to the nearest fiber optic node (meters) (less than or equal)
    population_density_lte: filters.NumberFilter = filters.NumberFilter(
        field_name="population_density",
        lookup_expr="lte",
        help_text=_("Filter by population density (population per ~30 square meters) less than or equal i.e `>=`."),
    )

    class Meta:

        model = PopulationDensityHD
        fields = [
            "country",
            "country_in",
            "administrative_area",
            "administrative_area_in",
            "population_density_gte",
            "population_density_lte",
        ]
