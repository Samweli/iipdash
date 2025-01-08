from typing import List, Type

from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.filters import BaseFilterBackend, OrderingFilter, SearchFilter

from ..models import CellTower
from .openapi import examples
from .serializers import CellTowerSerializer

__all__ = ["CellTowerViewSet"]


@extend_schema_view(
    list=extend_schema(
        description=_("Retrieve a list of cellular towers, with optional search and ordering."),
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

    #: A default queryset for retrieving `CellTower` objects.
    queryset: QuerySet[CellTower] = CellTower.objects.select_related("administrative_area").order_by("-created_at")

    #: A serializer class for handling `CellTower` objects.
    serializer_class: Type[CellTowerSerializer] = CellTowerSerializer

    #: A field used to retrieve a specific `CellTower` object.
    lookup_field: str = "uuid"

    #: A list of scope-based permissions required for access.
    required_scopes: List[str] = ["default"]

    #: A list of filters applied to the queryset.
    filter_backends: List[Type[BaseFilterBackend]] = [
        SearchFilter,
        OrderingFilter,
    ]

    #: A list of fields that can be searched via query parameters.
    search_fields: List[str] = ["network_type", "mcc", "range"]

    #: A list of fields that can be used for ordering results.
    ordering_fields: List[str] = ["network_type", "mcc", "range", "created_at", "updated_at"]
