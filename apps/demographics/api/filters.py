from typing import List, Type

from django.utils.translation import gettext_lazy as _

from django_filters import rest_framework as filters

from ..models import PopulationDensityHD, RelativeWealthIndex

__all__ = ["PopulationDensityHDFilter", "RelativeWealthIndexFilter"]


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


class RelativeWealthIndexFilter(filters.FilterSet):
    """
    FilterSet for the :class:`demographics.models.RelativeWealthIndex` model.

    This filter allows filtering `RelativeWealthIndex` objects based on specific
    fields.

    Examples:
        Filter by country code (exact match):
            `/api/demographics/relative-wealth-index/?country=MW`

        Filter by multiple country codes (in comparison):
            `/api/demographics/relative-wealth-index/?country_in=MW,ZM`

        Filter by administrative area UUID (exact match):
            `/api/demographics/relative-wealth-index/?administrative_area=04bcbe53-
            98da-4ff5-96a8-d626c6da45cc`

        Filter by multiple administrative area UUIDs (in comparison):
            `/api/demographics/relative-wealth-index/?administrative_area_in=04bcbe53-
            98da-4ff5-96a8-d626c6da45cc,032ffe37-67d6-40d4-a65d-144f12bbd493`

        Filter by relative wealth index (greater than or equal):
            `/api/demographics/relative-wealth-index/?rwi_gte=5216`

        Filter by relative wealth index (less than or equal):
            `/api/demographics/relative-wealth-index/?rwi_lte=5216`

    Attributes:
        country (:class:`django_filters.rest_framework.filters.CharFilter`):
            A filter for matching the `administrative_area__country` field
            of the `RelativeWealthIndex` model using `exact, case-insensitive` comparison.

        country_in (:class:`django_filters.rest_framework.filters.BaseInFilter`):
            A filter for matching multiple `administrative_area__country` field
            of the `RelativeWealthIndex` model using `in` comparison.

        administrative_area (:class:`django_filters.rest_framework.filters.UUIDFilter`):
            A filter for matching the `administrative_area__uuid` field of
            the `RelativeWealthIndex` model using `uuid equal` comparison.

        administrative_area_in (:class:`django_filters.rest_framework.filters.BaseInFilter`):
            A filter for matching multiple `administrative_area__uuid` field of
            the `RelativeWealthIndex` model using `in` comparison.

        rwi_gte (:class:`django_filters.rest_framework.filters.NumberFilter`):
            A filter for matching the `rwi` field of the `RelativeWealthIndex`
            model using `gte` comparison.

        rwi_lte (:class:`django_filters.rest_framework.filters.NumberFilter`):
            A filter for matching the `rwi` field of the `RelativeWealthIndex`
            model using `lte` comparison.
    """

    #: Filter by country code (exact match, case-insensitive)
    country: filters.CharFilter = filters.CharFilter(
        field_name="administrative_area__country",
        lookup_expr="iexact",
        help_text=_("Filter by country code."),
    )

    #: Filter by multiple country codes
    country_in: filters.BaseInFilter = filters.BaseInFilter(
        field_name="administrative_area__country",
        help_text=_("Filter by multiple country codes."),
    )

    #: Filter by administrative area UUID (exact match)
    administrative_area: filters.UUIDFilter = filters.UUIDFilter(
        field_name="administrative_area__uuid",
        help_text=_("Filter by administrative area UUID."),
    )

    #: Filter by multiple administrative area UUIDs
    administrative_area_in: filters.BaseInFilter = filters.BaseInFilter(
        field_name="administrative_area__uuid",
        help_text=_("Filter by multiple administrative area UUIDs."),
    )

    #: Filter by administrative area level (exact match)
    administrative_area_level: filters.NumberFilter = filters.NumberFilter(
        field_name="administrative_area__depth",
        help_text=_("Filter by administrative area level."),
    )

    #: Filter by relative wealth index (greater than or equal)
    rwi_gte: filters.NumberFilter = filters.NumberFilter(
        field_name="rwi",
        lookup_expr="gte",
        help_text=_("Filter by relative wealth index greater than or equal i.e `>=`."),
    )

    #: Filter by relative wealth index (less than or equal)
    rwi_lte: filters.NumberFilter = filters.NumberFilter(
        field_name="rwi",
        lookup_expr="lte",
        help_text=_("Filter by relative wealth index less than or equal i.e `<=`."),
    )

    class Meta:
        """
        Metadata for the :class:`RelativeWealthIndexFilter`.

        Attributes:
            model (Type[RelativeWealthIndex]):
                A Django model associated with this filter.
                In this case, it's the :class:`RelativeWealthIndex` model.

            fields (List[str]):
                A list of field names (i.e query parameters) available for filtering.
        """

        model: Type[RelativeWealthIndex] = RelativeWealthIndex
        fields: List[str] = [
            "country",
            "country_in",
            "administrative_area",
            "administrative_area_in",
            "administrative_area_level",
            "rwi_gte",
            "rwi_lte",
        ]
