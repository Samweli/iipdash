from typing import List, Type

from django_filters import rest_framework as filters

from ..models import Category

__all__ = ["CategoryFilter"]


class CategoryFilter(filters.FilterSet):
    """
    FilterSet for the :class:`education.models.Category` model.

    This filter allows filtering educational institution `Category` objects
    based on specific fields.

    Examples:
        Filtering by name (partial match, case-insensitive):
            `/api/education/categories/?name=uni`

        Filtering by code (exact match, case-insensitive):
            `/api/education/categories/?code=university`

    Attributes:
        name (:class:`django_filters.rest_framework.filters.CharFilter`):
            A filter for matching the `name` field of the `Category` model
            using a case-insensitive partial match.

        code (:class:`django_filters.rest_framework.filters.CharFilter`):
            A filter for matching the `code` field of the `Category` model
            using an exact, case-insensitive comparison.
    """

    #: Filter by name (partial match, case-insensitive)
    name: filters.CharFilter = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
    )

    #: Filter by code (exact match, case-insensitive)
    code: filters.CharFilter = filters.CharFilter(
        field_name="code",
        lookup_expr="iexact",
    )

    class Meta:
        """
        Metadata for the :class:`CategoryFilter`.

        Attributes:
            model (Type[Category]):
                A Django model associated with this filter.
                In this case, it's the :class:`Category` model.

            fields (List[str]):
                A list of field names available for filtering.
        """

        model: Type[Category] = Category
        fields: List[str] = ["name", "code"]
