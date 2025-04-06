from typing import List, Type

from django.utils.translation import gettext_lazy as _

from django_filters import rest_framework as filters

from core.api.filters import EmptyValueFilter

from ..models import CellTower, FiberOptic, MobileCoverage

__all__ = ["CellTowerFilter", "FiberOpticFilter", "MobileCoverageFilter"]


class CellTowerFilter(filters.FilterSet):
    """
    FilterSet for the :class:`infrastructure.models.CellTower` model.

    This filter allows filtering `CellTower` objects based on specific
    fields.

    Examples:
        Filtering by network type (exact match, case-insensitive):
            `/api/infrastructure/cell-towers/?network_type=GSM`

        Filtering by mobile country code (exact match):
            `/api/infrastructure/cell-towers/?mcc=645`

        Filter by estimated coverage range (greater than or equal):
            `/api/infrastructure/cell-towers/?range_gte=5216`

        Filter by estimated coverage range (less than or equal):
            `/api/infrastructure/cell-towers/?range_lte=5216`

        Filter by multiple administrative area UUIDs (in comparison):
            `/api/infrastructure/cell-towers/?administrative_area_in=04bcbe53-
            98da-4ff5-96a8-d626c6da45cc,032ffe37-67d6-40d4-a65d-144f12bbd493`

        Filter by multiple country codes (in comparison):
            `/api/infrastructure/cell-towers/?country_in=MW,ZM`

    Attributes:
        network_type (:class:`django_filters.rest_framework.filters.CharFilter`):
            A filter for matching the `network_type` field of the `CellTower`
            model using an exact, case-insensitive comparison.

        mcc (:class:`django_filters.rest_framework.filters.NumberFilter`):
            A filter for matching the `mcc` field of the `CellTower`
            model using `equal` comparison.

        range_gte (:class:`django_filters.rest_framework.filters.NumberFilter`):
            A filter for matching the `range` field of the `CellTower`
            model using `gte` comparison.

        range_lte (:class:`django_filters.rest_framework.filters.NumberFilter`):
            A filter for matching the `range` field of the `CellTower`
            model using `lte` comparison.

        administrative_area_in (:class:`django_filters.rest_framework.filters.BaseInFilter`):
            A filter for matching multiple `administrative_area__uuid` field of
            the `CellTower` model using `in` comparison.

        country_in (:class:`django_filters.rest_framework.filters.BaseInFilter`):
            A filter for matching multiple `administrative_area__country` field
            of the `CellTower` model using `in` comparison.
    """

    #: Filter by network_type (exact match, case-insensitive)
    network_type: filters.CharFilter = filters.CharFilter(
        field_name="network_type",
        lookup_expr="iexact",
        help_text=_("Filter by network type e.g., `GSM`, `UMTS`, `LTE`, `CDMA`."),
    )

    #: Filter by mobile country code (exact match)
    mcc: filters.NumberFilter = filters.NumberFilter(
        field_name="mcc",
        help_text=_("Filter by mobile country code e.g., `650` for Malawi."),
    )

    #: Filter by estimated coverage range (greater than or equal)
    range_gte: filters.NumberFilter = filters.NumberFilter(
        field_name="range",
        lookup_expr="gte",
        help_text=_("Filter by estimated coverage range greater than or equal i.e `>=`."),
    )

    #: Filter by estimated coverage range (less than or equal)
    range_lte: filters.NumberFilter = filters.NumberFilter(
        field_name="range",
        lookup_expr="lte",
        help_text=_("Filter by estimated coverage range less than or equal i.e `<=`."),
    )

    #: Filter by multiple administrative area UUIDs
    administrative_area_in: filters.BaseInFilter = filters.BaseInFilter(
        field_name="administrative_area__uuid",
        help_text=_("Filter by multiple administrative area UUIDs."),
    )

    #: Filter by multiple country codes
    country_in: filters.BaseInFilter = filters.BaseInFilter(
        field_name="administrative_area__country",
        help_text=_("Filter by multiple country codes."),
    )

    class Meta:
        """
        Metadata for the :class:`CellTowerFilter`.

        Attributes:
            model (Type[CellTower]):
                A Django model associated with this filter.
                In this case, it's the :class:`CellTower` model.

            fields (List[str]):
                A list of field names available for filtering.
        """

        model: Type[CellTower] = CellTower
        fields: List[str] = [
            "network_type",
            "mcc",
            "range_gte",
            "range_lte",
            "administrative_area_in",
        ]


class FiberOpticFilter(filters.FilterSet):
    """
    FilterSet for the :class:`infrastructure.models.FiberOptic` model.

    This filter allows filtering `FiberOptic` objects based on specific
    fields.

    Examples:
        Filtering by country (exact match, case-insensitive):
            `/api/infrastructure/fiber-optics/?country=MW`

        Filtering by name (partial match, case-insensitive):
            `/api/infrastructure/fiber-optics/?name=fiber`

        Filter by multiple administrative area UUIDs (in comparison):
            `/api/infrastructure/fiber-optics/?administrative_area_in=04bcbe53-
            98da-4ff5-96a8-d626c6da45cc,032ffe37-67d6-40d4-a65d-144f12bbd493`

        Filter by multiple country codes (in comparison):
            `/api/infrastructure/fiber-optics/?country_in=MW,ZM`

        Filtering by network type (exact match, case-insensitive):
            `/api/infrastructure/fiber-optics/?status=operational`

    Attributes:
        name (:class:`django_filters.rest_framework.filters.CharFilter`):
            A filter for matching the `name` field of the `FiberOptic` model
            using a case-insensitive partial match.

        administrative_area_in (:class:`django_filters.rest_framework.filters.BaseInFilter`):
            A filter for matching multiple `administrative_area__uuid` field of
            the `FiberOptic` model using `in` comparison.

        country_in (:class:`django_filters.rest_framework.filters.BaseInFilter`):
            A filter for matching multiple `administrative_area__country` field
            of the `FiberOptic` model using `in` comparison.

        status (:class:`django_filters.rest_framework.filters.CharFilter`):
            A filter for matching the `status` field of the `FiberOptic`
            model using an exact, case-insensitive comparison.
    """

    #: Filter by name (partial match, case-insensitive)
    name: filters.CharFilter = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        help_text=_("Filter by name."),
    )

    #: Filter by multiple administrative area UUIDs
    administrative_area_in: filters.BaseInFilter = filters.BaseInFilter(
        field_name="administrative_area__uuid",
        help_text=_("Filter by multiple administrative area UUIDs."),
    )

    #: Filter by multiple country codes
    country_in: filters.BaseInFilter = filters.BaseInFilter(
        field_name="administrative_area__country",
        help_text=_("Filter by multiple country codes."),
    )

    administrative_area_level = filters.NumberFilter(
        field_name="administrative_area__depth",
        help_text=_("Filter by administrative area level."),
    )

    #: Filter by operational status (exact match, case-insensitive)
    status: filters.ChoiceFilter = filters.ChoiceFilter(
        field_name="status",
        choices=FiberOptic.FiberOpticStatus.choices,
        lookup_expr="iexact",
        help_text=_("Filter by operational status."),
    )

    class Meta:
        """
        Metadata for the :class:`FiberOpticFilter`.

        Attributes:
            model (Type[FiberOptic]):
                A Django model associated with this filter.
                In this case, it's the :class:`FiberOptic` model.

            fields (List[str]):
                A list of field names available for filtering.
        """

        model: Type[FiberOptic] = FiberOptic
        fields: List[str] = ["name", "administrative_area_in", "country_in", "status"]


class MobileCoverageFilter(filters.FilterSet):

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

    administrative_area_level = filters.NumberFilter(field_name="administrative_area__depth")

    network_generation = filters.UUIDFilter(field_name="network_generation__uuid")
    network_generation_code = filters.CharFilter(field_name="network_generation__code")

    population_covered_gte = filters.NumberFilter(
        field_name="population_covered",
        lookup_expr="gte",
        help_text=_("minimum population covered"),
    )

    population_covered_lte = filters.NumberFilter(
        field_name="population_covered",
        lookup_expr="lte",
        help_text=_("maximum population covered"),
    )

    population_uncovered_gte = filters.NumberFilter(
        field_name="population_uncovered",
        lookup_expr="gte",
        help_text=_("minimum population not covered"),
    )

    population_uncovered_lte = filters.NumberFilter(
        field_name="population_uncovered",
        lookup_expr="lte",
        help_text=_("maximum population not covered"),
    )

    population_covered_percent_gte = filters.NumberFilter(
        field_name="population_covered_percent",
        lookup_expr="gte",
        help_text=_("minimum population covered"),
    )

    population_covered_percent_lte = filters.NumberFilter(
        field_name="population_covered_percent",
        lookup_expr="lte",
        help_text=_("maximum percentage of population covered"),
    )

    population_uncovered_percent_gte = filters.NumberFilter(
        field_name="population_uncovered_percent",
        lookup_expr="gte",
        help_text=_("minimum percentage of population not covered"),
    )

    population_uncovered_percent_lte = filters.NumberFilter(
        field_name="population_uncovered_percent",
        lookup_expr="lte",
        help_text=_("maximum percentage of population not covered"),
    )

    tiff_empty = EmptyValueFilter(field_name=_("tiff"))

    class Meta:

        model = MobileCoverage
        fields = [
            "country",
            "country_in",
            "administrative_area",
            "administrative_area_in",
            "network_generation",
            "network_generation_code",
            "population_covered_gte",
            "population_covered_lte",
            "population_uncovered_gte",
            "population_uncovered_lte",
            "population_covered_percent_gte",
            "population_covered_percent_lte",
            "population_uncovered_percent_gte",
            "population_uncovered_percent_lte",
        ]
