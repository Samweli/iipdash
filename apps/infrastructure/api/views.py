from typing import List, Type

from django.conf import settings
from django.contrib.gis.db.models import MultiLineStringField, PointField
from django.db.models import F, QuerySet
from django.db.models.functions import Cast
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import BaseFilterBackend, OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework_gis.pagination import GeoJsonPagination
from vectortiles.backends.postgis import VectorLayer
from vectortiles.rest_framework.renderers import MVTRenderer

from core.api.filters import DistanceToPointFilter, InBBoxFilter, TMSTileFilter
from core.api.mixins import CSVDownloadMixin

from ..models import CellTower, FiberOptic, FiberOpticNode, NetworkGeneration
from .filters import CellTowerFilter, FiberOpticFilter
from .openapi import examples
from .serializers import (
    CellTowerCSVSerializer,
    CellTowerSerializer,
    FiberOpticCSVSerializer,
    FiberOpticNodeCSVSerializer,
    FiberOpticNodeSerializer,
    FiberOpticSerializer,
    NetworkGenerationSerializer,
)

__all__ = ["CellTowerViewSet", "FiberOpticViewSet"]

MVT_CACHE_ALIAS = settings.CACHE_MVT_ALIAS
MVT_CACHE_TIMEOUT = settings.CACHE_TIMEOUTS["mvt"]


@extend_schema_view(
    list=extend_schema(
        summary=_("Mobile Network Generations"),
        description=_("Retrieve a list of mobile network generations."),
    ),
    retrieve=extend_schema(
        summary=_("Mobile Network Generation"),
        description=_("Retrieve details of a specific mobile network generation."),
    ),
)
class NetworkGenerationViewSet(viewsets.ReadOnlyModelViewSet):
    """Mobile Network Generations endpoint."""

    serializer_class = NetworkGenerationSerializer
    lookup_field: str = "uuid"
    required_scopes: List[str] = ["default"]
    queryset = NetworkGeneration.objects.all().order_by("id")


@extend_schema_view(
    list=extend_schema(
        description=_(
            "Retrieve a list of cellular towers, with optional searching, filtering, ordering and pagination."
        ),
        summary=_("Cellular Towers"),
        examples=examples.cell_tower_list_examples,
    ),
    retrieve=extend_schema(
        description=_("Retrieve details of a specific cellular tower."),
        summary=_("Cellular Tower"),
        examples=examples.cell_tower_retrieve_examples,
    ),
    download=extend_schema(summary=_("Cellular Towers CSV")),
    tile=extend_schema(summary=_("Cellular Towers Vector Tiles")),
)
class CellTowerViewSet(CSVDownloadMixin, VectorLayer, viewsets.ReadOnlyModelViewSet):
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
        InBBoxFilter,
        TMSTileFilter,
        DistanceToPointFilter,
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

    #: A `CellTower` geometry field used in performing bounding box filtering
    #: on the queryset of `CellTower` objects via query parameters
    #: (i.e., `?in_bbox=<bbox>`).
    bbox_filter_field: str = "geometry"

    #: Whether to include `CellTower` objects that overlap the bounding box
    #: on the queryset.
    bbox_filter_include_overlapping: bool = False

    #: A `CellTower` geometry field used in filtering queryset of `CellTower`
    #: objects based on their distance from a specific point via query
    #: parameters (i.e., `?point=<x,y>&radius=<distance>`).
    distance_filter_field: str = "geometry"

    #: Whether to convert the distance value to meters before filtering
    #: queryset of `CellTower` objects based on their distance from a
    #: specific point
    distance_filter_convert_meters: bool = True

    csv_serializer_class = CellTowerCSVSerializer

    #: Vector tiles layer ID
    id = "cell-towers"

    #: A tuple of fields to be included in vector tiles data.
    tile_fields = (
        "uuid",
        "network_type",
        "mcc",
        "location_is_approximate",
        "range",
        "country",
        "administrative_area_uuid",
        "administrative_area_name",
    )

    #: A default queryset for retrieving `CellTower` objects.
    queryset: QuerySet[CellTower] = CellTower.objects.select_related("administrative_area").order_by("-created_at")

    def get_vector_tile_queryset(self, *args, **kwargs):
        """Returns a queryset used to generate vector tiles."""

        queryset = self.get_queryset().annotate(
            geom=Cast("geometry", PointField()),
            country=F("administrative_area__country"),
            administrative_area_uuid=F("administrative_area__uuid"),
            administrative_area_name=F("administrative_area__name"),
        )

        queryset = self.filter_queryset(queryset)

        return queryset

    @action(
        detail=False,
        methods=["get"],
        name="Download Cell Towers CSV",
        url_path="download",
        url_name="list-download",
    )
    def download(self, request, *args, **kwargs):
        """Download Cell Towers as CSV file."""

        return self.export_csv(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        renderer_classes=(MVTRenderer,),
        url_path=r"tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).mvt",
        url_name="tile",
    )
    @method_decorator(cache_page(MVT_CACHE_TIMEOUT, key_prefix="mvt:cell-towers", cache=MVT_CACHE_ALIAS))
    def tile(self, request, *args, **kwargs):
        """Provides Mapbox Vector Tiles for cell towers"""
        return Response(self.get_tile(x=int(kwargs.get("x")), y=int(kwargs.get("y")), z=int(kwargs.get("z"))))


@extend_schema_view(
    list=extend_schema(
        description=_(
            "Retrieve a list of fiber optics networks, with optional searching, filtering, ordering and pagination."
        ),
        summary=_("Fiber Optic Networks"),
        examples=examples.fiber_optic_list_examples,
    ),
    retrieve=extend_schema(
        description=_("Retrieve details of a specific fiber optic network."),
        summary=_("Fiber Optic Network"),
        examples=examples.fiber_optic_retrieve_examples,
    ),
    tile=extend_schema(summary=_("Fiber Optic Networks Vector Tiles")),
    download=extend_schema(summary=_("Fiber Optic Networks CSV")),
)
class FiberOpticViewSet(CSVDownloadMixin, VectorLayer, viewsets.ReadOnlyModelViewSet):
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
        InBBoxFilter,
        TMSTileFilter,
        DistanceToPointFilter,
    ]

    #: A custom filter for applying complex filters to the queryset of
    #: `FiberOptic` objects.
    filterset_class: Type[FiberOpticFilter] = FiberOpticFilter

    #: A list of fields that are used for to apply full-text search
    #: via query parameters to the queryset of `FiberOptic` objects
    #: (i.e., `?q=<term>`).
    search_fields: List[str] = ["name"]

    #: A list of fields that are used for ordering the queryset of
    #: `FiberOptic` objects (e.g., `?ordering=<field>`).
    ordering_fields: List[str] = ["name", "created_at", "updated_at"]

    #: A `FiberOptic` geometry field used in performing bounding box filtering
    #: on the queryset of `FiberOptic` objects via query parameters
    #: (i.e., `?in_bbox=<bbox>`).
    bbox_filter_field: str = "geometry"

    #: Whether to include `FiberOptic` objects that overlap the bounding box
    #: on the queryset.
    bbox_filter_include_overlapping: bool = False

    #: A `FiberOptic` geometry field used in filtering queryset of `FiberOptic`
    #: objects based on their distance from a specific point via query
    #: parameters (i.e., `?point=<x,y>&radius=<distance>`).
    distance_filter_field: str = "geometry"

    #: Whether to convert the distance value to meters before filtering
    #: queryset of `FiberOptic` objects based on their distance from a
    #: specific point
    distance_filter_convert_meters: bool = True

    #: A default queryset for retrieving `FiberOptic` objects.
    queryset: QuerySet[FiberOptic] = FiberOptic.objects.select_related("administrative_area").order_by("-created_at")

    #: Vector tiles layer ID
    id = "fiber-optics"

    #: A tuple of fields to be included in vector tiles data.
    tile_fields = (
        "uuid",
        "name",
        "country",
        "status",
        "operator_name",
        "administrative_area_uuid",
        "administrative_area_name",
    )

    csv_serializer_class = FiberOpticCSVSerializer

    def get_vector_tile_queryset(self, *args, **kwargs):
        """Returns a queryset used to generate vector tiles."""

        queryset = self.get_queryset().annotate(
            geom=Cast("geometry", MultiLineStringField()),
            country=F("administrative_area__country"),
            administrative_area_uuid=F("administrative_area__uuid"),
            administrative_area_name=F("administrative_area__name"),
        )

        queryset = self.filter_queryset(queryset)

        return queryset

    @action(
        detail=False,
        methods=["get"],
        name="Download Fiber Optic networks CSV",
        url_path="download",
        url_name="list-download",
    )
    def download(self, request, *args, **kwargs):
        """Download Fiber Optic networks as CSV file."""

        return self.export_csv(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        renderer_classes=(MVTRenderer,),
        url_path=r"tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).mvt",
        url_name="tile",
    )
    @method_decorator(cache_page(MVT_CACHE_TIMEOUT, key_prefix="mvt:fiber-optics", cache=MVT_CACHE_ALIAS))
    def tile(self, request, *args, **kwargs):
        """Provides Mapbox Vector Tiles for fiber optic networks"""
        return Response(self.get_tile(x=int(kwargs.get("x")), y=int(kwargs.get("y")), z=int(kwargs.get("z"))))


@extend_schema_view(
    list=extend_schema(
        summary=_("Fiber Optic Nodes"),
        description=_("Retrieve a list of fiber optics nodes."),
    ),
    retrieve=extend_schema(
        summary=_("Fiber Optic Node"),
        description=_("Retrieve details of a specific fiber optic network."),
    ),
    tile=extend_schema(summary=_("Fiber Optic Node Vector Tiles")),
    download=extend_schema(summary=_("Fiber Optic Node CSV")),
)
class FiberOpticNodeViewSet(CSVDownloadMixin, VectorLayer, viewsets.ReadOnlyModelViewSet):
    """Fiber Optic Node endpoint"""

    serializer_class = FiberOpticNodeSerializer
    pagination_class = GeoJsonPagination
    lookup_field = "uuid"
    required_scopes = ["default"]

    #: A list of filter backends for applying search and order filters
    #: to the queryset of `FiberOptic` objects.
    filter_backends: List[Type[BaseFilterBackend]] = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
        InBBoxFilter,
        TMSTileFilter,
        DistanceToPointFilter,
    ]

    filter_fields = ["node_type", "administrative_area"]

    #: A `FiberOptic` geometry field used in performing bounding box filtering
    #: on the queryset of `FiberOptic` objects via query parameters
    #: (i.e., `?in_bbox=<bbox>`).
    bbox_filter_field: str = "geometry"
    bbox_filter_include_overlapping: bool = False

    #: A `FiberOptic` geometry field used in filtering queryset of `FiberOptic`
    #: objects based on their distance from a specific point via query
    #: parameters (i.e., `?point=<x,y>&radius=<distance>`).
    distance_filter_field = "geometry"
    distance_filter_convert_meters = True

    queryset = FiberOpticNode.objects.select_related("administrative_area").order_by("-created_at")

    #: Vector tiles layer ID
    id = "fiber-nodes"

    #: A tuple of fields to be included in vector tiles data.
    tile_fields = (
        "uuid",
        "name",
        "node_type",
        "country",
        "administrative_area_uuid",
        "administrative_area_name",
    )

    csv_serializer_class = FiberOpticNodeCSVSerializer

    def get_vector_tile_queryset(self, *args, **kwargs):
        """Returns a queryset used to generate vector tiles."""

        queryset = self.get_queryset().annotate(
            geom=Cast("geometry", MultiLineStringField()),
            country=F("administrative_area__country"),
            administrative_area_uuid=F("administrative_area__uuid"),
            administrative_area_name=F("administrative_area__name"),
        )

        queryset = self.filter_queryset(queryset)

        return queryset

    @action(
        detail=False,
        methods=["get"],
        name="Download Fiber Optic nodes CSV",
        url_path="download",
        url_name="list-download",
    )
    def download(self, request, *args, **kwargs):
        """Download Fiber Optic nodes as CSV file."""

        return self.export_csv(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        renderer_classes=(MVTRenderer,),
        url_path=r"tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).mvt",
        url_name="tile",
    )
    @method_decorator(cache_page(MVT_CACHE_TIMEOUT, key_prefix="mvt:fiber-nodes", cache=MVT_CACHE_ALIAS))
    def tile(self, request, *args, **kwargs):
        """Provides Mapbox Vector Tiles for fiber optic nodes"""
        return Response(self.get_tile(x=int(kwargs.get("x")), y=int(kwargs.get("y")), z=int(kwargs.get("z"))))
