from typing import List, Type

from django.utils.translation import gettext_lazy as _

from django_filters import rest_framework as filters

from ..models import Category, Institution, Ownership

__all__ = ["CategoryFilter", "OwnershipFilter", "InstitutionFilter"]


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
        help_text=_("Filter by name."),
    )

    #: Filter by code (exact match, case-insensitive)
    code: filters.CharFilter = filters.CharFilter(
        field_name="code",
        lookup_expr="iexact",
        help_text=_("Filter by code."),
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


class OwnershipFilter(filters.FilterSet):
    """
    FilterSet for the :class:`education.models.Ownership` model.

    This filter allows filtering educational institution `Ownership` objects
    based on specific fields.

    Examples:
        Filtering by name (partial match, case-insensitive):
            `/api/education/ownerships/?name=pub`

        Filtering by code (exact match, case-insensitive):
            `/api/education/ownerships/?code=public`

    Attributes:
        name (:class:`django_filters.rest_framework.filters.CharFilter`):
            A filter for matching the `name` field of the `Ownership` model
            using a case-insensitive partial match.

        code (:class:`django_filters.rest_framework.filters.CharFilter`):
            A filter for matching the `code` field of the `Ownership` model
            using an exact, case-insensitive comparison.
    """

    #: Filter by name (partial match, case-insensitive)
    name: filters.CharFilter = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        help_text=_("Filter by name."),
    )

    #: Filter by code (exact match, case-insensitive)
    code: filters.CharFilter = filters.CharFilter(
        field_name="code",
        lookup_expr="iexact",
        help_text=_("Filter by code."),
    )

    class Meta:
        """
        Metadata for the :class:`OwnershipFilter`.

        Attributes:
            model (Type[Ownership]):
                A Django model associated with this filter.
                In this case, it's the :class:`Ownership` model.

            fields (List[str]):
                A list of field names available for filtering.
        """

        model: Type[Ownership] = Ownership
        fields: List[str] = ["name", "code"]


class InstitutionFilter(filters.FilterSet):
    """
    FilterSet for the :class:`education.models.Institution` model.

    This filter allows filtering educational `Institution` objects
    based on specific fields.

    Examples:
        Filter by multiple country codes:
            `/api/education/institutions/?country_in=MW,ZM`

        Filtering by name (partial match, case-insensitive):
            `/api/education/institutions/?name=university+of+malawi`

        Filtering by code (exact match, case-insensitive):
            `/api/education/institutions/?code=UMCM`

        Filter by multiple administrative area UUIDs (in comparison):
            `/api/education/institutions/?administrative_area_in=04bcbe53-98da-
            4ff5-96a8-d626c6da45cc,032ffe37-67d6-40d4-a65d-144f12bbd493`

        Filter by whether connected to electricity or not:
            `/api/education/institutions/?has_electricity=true`

        Filter by distance (in meters) to the nearest fiber optic node (greater than or equal):
            `/api/education/institutions/?fon_distance_gte=216`

    Attributes:
        country_in (:class:`django_filters.rest_framework.filters.BaseInFilter`):
            A filter for matching multiple `administrative_area__country` field
            of the `Institution` model using `in` comparison.

        category_in (:class:`django_filters.rest_framework.filters.BaseInFilter`):
            A filter for matching multiple `category__uuid` field of the
            `Institution` model using `in` comparison.

        name (:class:`django_filters.rest_framework.filters.CharFilter`):
            A filter for matching the `name` field of the `Institution` model
            using a case-insensitive partial match.

        ownership_in (:class:`django_filters.rest_framework.filters.BaseInFilter`):
            A filter for matching multiple `ownership__uuid` field of the
            `Institution` model using `in` comparison.

        code (:class:`django_filters.rest_framework.filters.CharFilter`):
            A filter for matching the `code` field of the `Institution` model
            using an exact, case-insensitive comparison.

        administrative_area_in (:class:`django_filters.rest_framework.filters.BaseInFilter`):
            A filter for matching multiple `administrative_area__uuid` field of
            the `Institution` model using `in` comparison.

        has_electricity (:class:`django_filters.rest_framework.filters.BooleanFilter`):
            A filter for matching the `has_electricity` field of the
            `Institution` model using a boolean match.

        has_fiber_optic (:class:`django_filters.rest_framework.filters.BooleanFilter`):
            A filter for matching the `has_fiber_optic` field of the
            `Institution` model using a boolean match.

        fon_distance_gte (:class:`django_filters.rest_framework.filters.NumberFilter`):
            A filter for matching the `fon_distance` field of the `Institution`
            model using `gte` comparison.

        fon_distance_lte (:class:`django_filters.rest_framework.filters.NumberFilter`):
            A filter for matching the `fon_distance` field of the `Institution`
            model using `lte` comparison.
    """

    #: Filter by multiple country codes
    country_in: filters.BaseInFilter = filters.BaseInFilter(
        field_name="administrative_area__country",
        help_text=_("Filter by multiple country codes."),
    )

    #: Filter by multiple category UUIDs
    category_in: filters.BaseInFilter = filters.BaseInFilter(
        field_name="category__uuid",
        help_text=_("Filter by multiple category UUIDs."),
    )

    #: Filter by name (partial match, case-insensitive)
    name: filters.CharFilter = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        help_text=_("Filter by name."),
    )

    #: Filter by multiple ownership UUIDs
    ownership_in: filters.BaseInFilter = filters.BaseInFilter(
        field_name="ownership__uuid",
        help_text=_("Filter by multiple ownership UUIDs."),
    )

    #: Filter by code (exact match, case-insensitive)
    code: filters.CharFilter = filters.CharFilter(
        field_name="code",
        lookup_expr="iexact",
        help_text=_("Filter by code."),
    )

    #: Filter by multiple administrative area UUIDs
    administrative_area_in: filters.BaseInFilter = filters.BaseInFilter(
        field_name="administrative_area__uuid",
        help_text=_("Filter by multiple administrative area UUIDs."),
    )

    #: Filter by whether connected to electricity or not
    has_electricity: filters.BooleanFilter = filters.BooleanFilter(
        field_name="has_electricity",
        help_text=_("Filter by whether connected to electricity or not."),
    )

    #: Filter by whether connected to fiber optic or not
    has_fiber_optic: filters.BooleanFilter = filters.BooleanFilter(
        field_name="has_fiber_optic",
        help_text=_("Filter by whether connected to fiber optic or not."),
    )

    #: Filter by distance (in meters) to the nearest fiber optic node (greater than or equal)
    fon_distance_gte: filters.NumberFilter = filters.NumberFilter(
        field_name="fon_distance",
        lookup_expr="gte",
        help_text=_(
            "Filter by distance (in meters) to the nearest fiber optic "
            "node (meters) greater than or equal i.e `>=`."
        ),
    )

    #: Filter by distance (in meters) to the nearest fiber optic node (meters) (less than or equal)
    fon_distance_lte: filters.NumberFilter = filters.NumberFilter(
        field_name="fon_distance",
        lookup_expr="lte",
        help_text=_("Filter by distance (in meters) to the nearest fiber optic node less than or equal i.e `<=`."),
    )

    class Meta:
        """
        Metadata for the :class:`InstitutionFilter`.

        Attributes:
            model (Type[Institution]):
                A Django model associated with this filter.
                In this case, it's the :class:`Institution` model.

            fields (List[str]):
                A list of field names available for filtering.
        """

        model: Type[Institution] = Institution
        fields: List[str] = [
            "country_in",
            "category_in",
            "ownership_in",
            "name",
            "code",
            "administrative_area_in",
            "has_electricity",
            "has_fiber_optic",
            "fon_distance_lte",
            "fon_distance_lte",
        ]
