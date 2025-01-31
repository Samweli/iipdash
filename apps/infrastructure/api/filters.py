from typing import List, Type

from django.utils.translation import gettext_lazy as _

from django_filters import rest_framework as filters

from ..models import CellTower, FiberOptic

__all__ = ["CellTowerFilter", "FiberOpticFilter"]


class CellTowerFilter(filters.FilterSet):
    """
    FilterSet for the :class:`infrastructure.models.CellTower` model.

    This filter allows filtering `CellTower` objects based on specific
    fields.

    Examples:
        Filtering by network type (exact match, case-insensitive):
            `/api/infrastructure/celltowers/?network_type=GSM`

        Filtering by mobile country code (exact match):
            `/api/infrastructure/celltowers/?mcc=645`

        Filter by estimated coverage range (greater than or equal):
            `/api/infrastructure/celltowers/?range_gte=5216`

        Filter by estimated coverage range (less than or equal):
            `/api/infrastructure/celltowers/?range_lte=5216`

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
        fields: List[str] = ["network_type", "mcc", "range_gte", "range_lte"]


class FiberOpticFilter(filters.FilterSet):
    """
    FilterSet for the :class:`infrastructure.models.FiberOptic` model.

    This filter allows filtering `FiberOptic` objects based on specific
    fields.

    Examples:
        Filtering by country (exact match, case-insensitive):
            `/api/infrastructure/fiberoptics/?country=MW`

        Filtering by name (partial match, case-insensitive):
            `/api/infrastructure/fiberoptics/?name=fiber`

    Attributes:
        country (:class:`django_filters.rest_framework.filters.CharFilter`):
            A filter for matching the `country` field of the `FiberOptic` model
            using an exact, case-insensitive comparison.

        name (:class:`django_filters.rest_framework.filters.CharFilter`):
            A filter for matching the `name` field of the `FiberOptic` model
            using a case-insensitive partial match.
    """

    #: Filter by country (exact match, case-insensitive)
    country: filters.CharFilter = filters.CharFilter(
        field_name="country",
        lookup_expr="iexact",
        help_text=_("Filter by country."),
    )

    #: Filter by name (partial match, case-insensitive)
    name: filters.CharFilter = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        help_text=_("Filter by name."),
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
        fields: List[str] = ["country", "name", "status"]
