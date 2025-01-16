from typing import List, Type

from django_filters import rest_framework as filters

from ..models import FiberOptic

__all__ = ["FiberOpticFilter"]


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
    )

    #: Filter by name (partial match, case-insensitive)
    name: filters.CharFilter = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
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
