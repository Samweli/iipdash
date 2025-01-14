from typing import List, Type

from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.filters import BaseFilterBackend, OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework_gis.pagination import GeoJsonPagination

from ..models import Category, Institution, Ownership
from .filters import CategoryFilter, OwnershipFilter
from .openapi import examples
from .serializers import CategorySerializer, InstitutionSerializer, OwnershipSerializer

__all__ = ["CategoryViewSet", "OwnershipViewSet", "InstitutionViewSet"]


@extend_schema_view(
    list=extend_schema(
        description=_(
            "Retrieve a list of educational institution categories, with"
            " optional searching, filtering, ordering and pagination."
        ),
        summary=_("List educational institution categories"),
        examples=examples.category_list_examples,
    ),
    retrieve=extend_schema(
        description=_("Retrieve details of a specific educational institution category."),
        summary=_("Retrieve educational institution category"),
        examples=examples.category_retrieve_examples,
    ),
)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for managing :class:`education.models.Category` objects.

    This viewset provides endpoints for:
    - Listing all educational institution categories (`list` endpoint).
    - Retrieving a specific educational institution category by UUID (`retrieve` endpoint).
    """

    #: A serializer class for converting `Category` objects to JSON format.
    serializer_class: Type[CategorySerializer] = CategorySerializer

    #: A pagination class to handle JSON format pagination for `Category` objects.
    pagination_class: Type[PageNumberPagination] = PageNumberPagination

    #: A lookup field used to retrieve a specific `Category` object.
    lookup_field: str = "uuid"

    #: A list of required OAuth2 scopes for accessing the `Category` API endpoints.
    required_scopes: List[str] = ["default"]

    #: A list of filter backends for applying search and order filters
    #: to the queryset of `Category` objects.
    filter_backends: List[Type[BaseFilterBackend]] = [
        SearchFilter,
        OrderingFilter,
    ]

    #: A custom filter for applying complex filters to the queryset of
    #: `Category` objects.
    filterset_class: Type[CategoryFilter] = CategoryFilter

    #: A list of fields that are used for to apply full-text search
    #: via query parameters to the queryset of `Category` objects
    #: (i.e., `?q=<term>`).
    search_fields: List[str] = ["name", "code"]

    #: A list of fields that are used for ordering the queryset of
    #: `Category` objects (e.g., `?ordering=<field>`).
    ordering_fields: List[str] = ["name", "created_at", "updated_at"]

    #: A default queryset for retrieving `Category` objects.
    queryset: QuerySet[Category] = Category.objects.all().order_by("-created_at")


@extend_schema_view(
    list=extend_schema(
        description=_(
            "Retrieve a list of educational institution ownerships, "
            "with optional searching, filtering, ordering and pagination."
        ),
        summary=_("List educational institution ownerships"),
        examples=examples.ownership_list_examples,
    ),
    retrieve=extend_schema(
        description=_("Retrieve details of a specific educational institution ownership."),
        summary=_("Retrieve educational institution ownership"),
        examples=examples.ownership_retrieve_examples,
    ),
)
class OwnershipViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for managing :class:`education.models.Ownership` objects.

    This viewset provides endpoints for:
    - Listing all educational institution ownerships (`list` endpoint).
    - Retrieving a specific educational institution ownership by UUID (`retrieve` endpoint).
    """

    #: A serializer class for converting `Ownership` objects to JSON format.
    serializer_class: Type[OwnershipSerializer] = OwnershipSerializer

    #: A pagination class to handle JSON format pagination for `Ownership` objects.
    pagination_class: Type[PageNumberPagination] = PageNumberPagination

    #: A lookup field used to retrieve a specific `Ownership` object.
    lookup_field: str = "uuid"

    #: A list of required OAuth2 scopes for accessing the `Ownership` API endpoints.
    required_scopes: List[str] = ["default"]

    #: A list of filter backends for applying search and order filters
    #: to the queryset of `Ownership` objects.
    filter_backends: List[Type[BaseFilterBackend]] = [
        SearchFilter,
        OrderingFilter,
    ]

    #: A custom filter for applying complex filters to the queryset of
    #: `Ownership` objects.
    filterset_class: Type[OwnershipFilter] = OwnershipFilter

    #: A list of fields that are used for to apply full-text search
    #: via query parameters to the queryset of `Ownership` objects
    #: (i.e., `?q=<term>`).
    search_fields: List[str] = ["name", "code"]

    #: A list of fields that are used for ordering the queryset of
    #: `Ownership` objects (e.g., `?ordering=<field>`).
    ordering_fields: List[str] = ["name", "created_at", "updated_at"]

    #: A default queryset for retrieving `Ownership` objects.
    queryset: QuerySet[Ownership] = Ownership.objects.all().order_by("-created_at")


@extend_schema_view(
    list=extend_schema(
        summary=_("List Education Institution"),
        description=_("Retrieve a list of education institutions."),
    ),
    retrieve=extend_schema(
        summary=_("Retrieve Education Institution"),
        description=_("Retrieve details of an education institution."),
    ),
)
class InstitutionViewSet(viewsets.ReadOnlyModelViewSet):
    """Education Institutions API endpoint"""

    serializer_class = InstitutionSerializer
    lookup_field = "uuid"
    required_scopes = ["default"]
    pagination_class = GeoJsonPagination

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at", "updated_at"]

    queryset = Institution.objects.select_related("category", "ownership", "administrative_area").order_by("name")
