from typing import List, Type

from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, viewsets

from ..models import Category, Ownership
from .serializers import CategorySerializer, OwnershipSerializer

__all__ = ["CategoryViewSet"]


@extend_schema_view(
    list=extend_schema(
        description=_("Retrieve a list of categories, with optional search and ordering."),
        summary=_("List categories"),
    ),
    retrieve=extend_schema(
        description=_("Retrieve details of a specific category."),
        summary=_("Retrieve category"),
    ),
)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for managing :class:`education.models.Category` objects.

    This viewset provides endpoints for:
    - Listing all categories (`list` endpoint).
    - Retrieving a specific category by UUID (`retrieve` endpoint).
    """

    #: A default queryset for retrieving `Category` objects.
    queryset: QuerySet[Category] = Category.objects.all().order_by("-created_at")

    #: A serializer class for handling `Category` objects.
    serializer_class: Type[CategorySerializer] = CategorySerializer

    #: A field used to retrieve a specific `Category` object.
    lookup_field: str = "uuid"

    #: A list of scope-based permissions required for access.
    required_scopes: List[str] = ["default"]

    #: A list of filters applied to the queryset.
    filter_backends: List[Type[filters.BaseFilterBackend]] = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    #: A list of fields that can be searched via query parameters.
    search_fields: List[str] = ["name", "code"]

    #: A list of fields that can be used for ordering results.
    ordering_fields: List[str] = ["name", "created_at", "updated_at"]


@extend_schema_view(
    list=extend_schema(
        description=_("Retrieve a list of ownerships, with optional search and ordering."),
        summary=_("List ownerships"),
    ),
    retrieve=extend_schema(
        description=_("Retrieve details of a specific ownership."),
        summary=_("Retrieve ownership"),
    ),
)
class OwnershipViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for managing :class:`education.models.Ownership` objects.

    This viewset provides endpoints for:
    - Listing all ownerships (`list` endpoint).
    - Retrieving a specific ownership by UUID (`retrieve` endpoint).
    """

    #: A default queryset for retrieving `Ownership` objects.
    queryset: QuerySet[Ownership] = Ownership.objects.all().order_by("-created_at")

    #: A serializer class for handling `Ownership` objects.
    serializer_class: Type[OwnershipSerializer] = OwnershipSerializer

    #: A field used to retrieve a specific `Ownership` object.
    lookup_field: str = "uuid"

    #: A list of scope-based permissions required for access.
    required_scopes: List[str] = ["default"]

    #: A list of filters applied to the queryset.
    filter_backends: List[Type[filters.BaseFilterBackend]] = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    #: A list of fields that can be searched via query parameters.
    search_fields: List[str] = ["name", "code"]

    #: A list of fields that can be used for ordering results.
    ordering_fields: List[str] = ["name", "created_at", "updated_at"]
