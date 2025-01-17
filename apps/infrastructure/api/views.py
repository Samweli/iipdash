from typing import List, Type

from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.filters import BaseFilterBackend, OrderingFilter, SearchFilter
from rest_framework_gis.pagination import GeoJsonPagination

from ..models import CellTower, FiberOptic
from .filters import CellTowerFilter, FiberOpticFilter
from .openapi import examples
from .serializers import CellTowerSerializer, FiberOpticSerializer

__all__ = ["CellTowerViewSet", "FiberOpticViewSet"]


@extend_schema_view(
    list=extend_schema(
        description=_(
            "Retrieve a list of cellular towers, with optional searching, filtering, ordering and pagination."
        ),
        summary=_("List cellular towers"),
        examples=examples.celltower_list_examples,
    ),
    retrieve=extend_schema(
        description=_("Retrieve details of a specific cellular tower."),
        summary=_("Retrieve cellular tower"),
        examples=examples.celltower_retrieve_examples,
    ),
)
class CellTowerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for managing :class:`infrastructure.models.CellTower` objects.

    This viewset provides endpoints for:
    - Listing all cellular towers (`list` endpoint).
    - Retrieving a specific cellular tower by UUID (`retrieve` endpoint).
    """

    #: A serializer class for converting `CellTower` objects to GeoJSON format.
    serializer_class: Type[CellTowerSerializer] = CellTowerSerializer

    #: A pagination class to handle GeoJSON format pagination for `CellTower` objects.
    pagination_class: Type[GeoJsonPagination] = GeoJsonPagination

    #: A lookup field used to retrieve a specific `CellTower` object.
    lookup_field: str = "uuid"

    #: A list of required OAuth2 scopes for accessing the `CellTower` API endpoints.
    required_scopes: List[str] = ["default"]

    #: A list of filter backends for applying search and order filters
    #: to the queryset of `CellTower` objects.
    filter_backends: List[Type[BaseFilterBackend]] = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    #: A custom filter for applying complex filters to the queryset of
    #: `CellTower` objects.
    filterset_class: Type[CellTowerFilter] = CellTowerFilter

    #: A list of fields that are used for to apply full-text search
    #: via query parameters to the queryset of `CellTower` objects
    #: (i.e., `?q=<term>`).
    search_fields: List[str] = ["network_type", "mcc", "range"]

    #: A list of fields that are used for ordering the queryset of
    #: `CellTower` objects (e.g., `?ordering=<field>`).
    ordering_fields: List[str] = ["network_type", "mcc", "range", "created_at", "updated_at"]

    #: A default queryset for retrieving `CellTower` objects.
    queryset: QuerySet[CellTower] = CellTower.objects.select_related("administrative_area").order_by("-created_at")


@extend_schema_view(
    list=extend_schema(
        description=_("Retrieve a list of fiber optics, with optional searching, filtering, ordering and pagination."),
        summary=_("List fiber optics"),
        examples=examples.fiberoptic_list_examples,
    ),
    retrieve=extend_schema(
        description=_("Retrieve details of a specific fiber optic."),
        summary=_("Retrieve fiber optic"),
        examples=examples.fiberoptic_retrieve_examples,
    ),
)
class FiberOpticViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for managing :class:`infrastructure.models.FiberOptic` objects.

    This viewset provides endpoints for:
    - Listing all fiber optics (`list` endpoint).
    - Retrieving a specific fiber optic by UUID (`retrieve` endpoint).
    """

    #: A serializer class for converting `FiberOptic` objects to GeoJSON format.
    serializer_class: Type[FiberOpticSerializer] = FiberOpticSerializer

    #: A pagination class to handle GeoJSON format pagination for `FiberOptic` objects.
    pagination_class: Type[GeoJsonPagination] = GeoJsonPagination

    #: A lookup field used to retrieve a specific `FiberOptic` object.
    lookup_field: str = "uuid"

    #: A list of required OAuth2 scopes for accessing the `FiberOptic` API endpoints.
    required_scopes: List[str] = ["default"]

    #: A list of filter backends for applying search and order filters
    #: to the queryset of `FiberOptic` objects.
    filter_backends: List[Type[BaseFilterBackend]] = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    #: A custom filter for applying complex filters to the queryset of
    #: `FiberOptic` objects.
    filterset_class: Type[FiberOpticFilter] = FiberOpticFilter

    #: A list of fields that are used for to apply full-text search
    #: via query parameters to the queryset of `FiberOptic` objects
    #: (i.e., `?q=<term>`).
    search_fields: List[str] = ["country", "name"]

    #: A list of fields that are used for ordering the queryset of
    #: `FiberOptic` objects (e.g., `?ordering=<field>`).
    ordering_fields: List[str] = ["country", "name", "created_at", "updated_at"]

    #: A default queryset for retrieving `FiberOptic` objects.
    queryset: QuerySet[FiberOptic] = FiberOptic.objects.select_related("administrative_area").order_by("-created_at")
