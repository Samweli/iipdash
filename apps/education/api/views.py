from typing import List, Type

from django.contrib.gis.db.models import PointField
from django.db.models import F, QuerySet
from django.db.models.functions import Cast
from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import BaseFilterBackend, OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_gis.pagination import GeoJsonPagination
from vectortiles.backends.postgis import VectorLayer
from vectortiles.rest_framework.renderers import MVTRenderer

from core.api.filters import DistanceToPointFilter, InBBoxFilter, TMSTileFilter
from core.api.mixins import CSVDownloadMixin

from ..models import Category, Institution, Ownership
from .filters import CategoryFilter, InstitutionFilter, OwnershipFilter
from .openapi import examples
from .serializers import CategorySerializer, InstitutionCSVSerializer, InstitutionSerializer, OwnershipSerializer

__all__ = ["CategoryViewSet", "OwnershipViewSet", "InstitutionViewSet"]


@extend_schema_view(
    list=extend_schema(
        description=_(
            "Retrieve a list of educational institution categories, with"
            " optional searching, filtering, ordering and pagination."
        ),
        summary=_("Education Institutions Categories"),
        examples=examples.category_list_examples,
    ),
    retrieve=extend_schema(
        description=_("Retrieve details of a specific educational institution category."),
        summary=_("Education Institutions Category"),
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
        DjangoFilterBackend,
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
        summary=_("Education Institutions Ownerships"),
        examples=examples.ownership_list_examples,
    ),
    retrieve=extend_schema(
        description=_("Retrieve details of a specific educational institution ownership."),
        summary=_("Education Institutions Ownership"),
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
        DjangoFilterBackend,
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
        summary=_("Education Institutions"),
        description=_("Retrieve a list of education institutions."),
    ),
    retrieve=extend_schema(
        summary=_("Education Institution"),
        description=_("Retrieve details of an education institution."),
    ),
    download=extend_schema(summary=_("Education Institutions CSV")),
    tile=extend_schema(summary=_("Education Institutions Vector Tiles")),
)
class InstitutionViewSet(CSVDownloadMixin, VectorLayer, viewsets.ReadOnlyModelViewSet):
    """Education Institutions API endpoint"""

    serializer_class = InstitutionSerializer
    lookup_field = "uuid"
    required_scopes = ["default"]
    pagination_class = GeoJsonPagination

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
        InBBoxFilter,
        TMSTileFilter,
        DistanceToPointFilter,
    ]
    filterset_class = InstitutionFilter
    search_fields = ["name"]
    ordering_fields = ["name", "created_at", "updated_at"]

    bbox_filter_field = "geometry"
    bbox_filter_include_overlapping = False
    distance_filter_field = "geometry"
    distance_filter_convert_meters = True

    csv_serializer_class = InstitutionCSVSerializer

    #: Vector tiles layer ID
    id = "education-institutions"

    #: A tuple of fields to be included in vector tiles data.
    tile_fields = (
        "uuid",
        "category_name",
        "name",
        "code",
        "ownership_name",
        "country",
        "has_electricity",
        "has_fiber_optic",
        "fon_distance",
        "administrative_area_uuid",
        "administrative_area_name",
    )

    def get_queryset(self):
        return Institution.objects.select_related("category", "ownership", "administrative_area").order_by("name")

    def get_vector_tile_queryset(self, *args, **kwargs):
        """Returns a queryset used to generate vector tiles."""

        queryset = self.get_queryset().annotate(
            geom=Cast("geometry", PointField()),
            category_uuid=F("category__uuid"),
            category_name=F("category__name"),
            ownership_uuid=F("ownership__uuid"),
            ownership_name=F("ownership__name"),
            country=F("administrative_area__country"),
            administrative_area_uuid=F("administrative_area__uuid"),
            administrative_area_name=F("administrative_area__name"),
        )

        queryset = self.filter_queryset(queryset)

        return queryset

    @action(
        detail=False,
        methods=["get"],
        name="Download Education Institution CSV",
        url_path="download",
        url_name="list-download",
    )
    def download(self, request, *args, **kwargs):
        """Download Education Institutions as CSV file."""

        return self.export_csv(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        renderer_classes=(MVTRenderer,),
        url_path=r"tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).mvt",
        url_name="tile",
    )
    def tile(self, request, *args, **kwargs):
        """Provides Mapbox Vector Tiles for eduction institutions"""
        return Response(self.get_tile(x=int(kwargs.get("x")), y=int(kwargs.get("y")), z=int(kwargs.get("z"))))
