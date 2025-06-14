from typing import List, Type

from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.db.models import F, QuerySet
from django.db.models.functions import Cast
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.filters import BaseFilterBackend, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.pagination import GeoJsonPagination
from vectortiles.backends.postgis import VectorLayer
from vectortiles.rest_framework.renderers import MVTRenderer

from core.api.filters import DistanceToPointFilter, InBBoxFilter, TMSTileFilter
from core.api.mixins import CSVDownloadMixin

from ..models import PopulationDensityHD, RelativeWealthIndex
from .filters import PopulationDensityHDFilter, RelativeWealthIndexFilter
from .serializers import PopulationDensityHDSerializer, RelativeWealthIndexCSVSerializer, RelativeWealthIndexSerializer

MVT_CACHE_ALIAS = settings.CACHE_MVT_ALIAS
MVT_CACHE_TIMEOUT = settings.CACHE_TIMEOUTS["mvt"]


@extend_schema_view(
    list=extend_schema(
        summary=_("Population Densities (HD)"),
        description=_("Retrieve a list of high resolution population densities."),
    ),
    retrieve=extend_schema(
        summary=_("Population Density (HD)"),
        description=_("Retrieve details of a high resolution population density."),
    ),
    tile=extend_schema(summary=_("High resolution population density vector tiles")),
)
class PopulationDensityHDViewSet(VectorLayer, ReadOnlyModelViewSet):
    """High resolution population density API endpoint."""

    serializer_class = PopulationDensityHDSerializer
    lookup_field = "uuid"
    required_scopes = ["default"]
    pagination_class = GeoJsonPagination

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PopulationDensityHDFilter
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    #: Vector tiles layer ID
    id = "population-density-hd"

    #: A tuple of fields to be included in vector tiles data.
    tile_fields = (
        "population_density",
        "administrative_area_uuid",
        "country",
    )
    tile_buffer = 64

    queryset = PopulationDensityHD.objects.all()

    def get_vector_tile_queryset(self, *args, **kwargs):
        """Returns a queryset used to generate vector tiles."""

        zoom = int(self.kwargs["z"])

        queryset = (
            self.get_queryset()
            .annotate(
                administrative_area_uuid=F("administrative_area__uuid"),
                country=F("administrative_area__country"),
            )
            .order_by()
        )

        # reduce features displayed at low zoom levels
        if zoom <= 7:
            queryset = queryset.filter(population_density__gte=20 - zoom)

        queryset = self.filter_queryset(queryset)

        return queryset

    @action(
        detail=False,
        methods=["get"],
        renderer_classes=(MVTRenderer,),
        url_path=r"tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).mvt",
        url_name="tile",
    )
    @method_decorator(cache_page(MVT_CACHE_TIMEOUT, key_prefix="mvt:population-density-hd", cache=MVT_CACHE_ALIAS))
    def tile(self, request, *args, **kwargs):
        """Provides Mapbox Vector Tiles for high resolution population density."""
        return Response(self.get_tile(x=int(kwargs.get("x")), y=int(kwargs.get("y")), z=int(kwargs.get("z"))))


@extend_schema_view(
    list=extend_schema(
        summary=_("Relative Wealth Indexes"),
        description=_(
            "Retrieve a list of relative wealth indexes, with optional searching, filtering, ordering and pagination."
        ),
    ),
    retrieve=extend_schema(
        summary=_("Relative Wealth Index"),
        description=_("Retrieve details of a specific relative wealth index."),
    ),
    tile=extend_schema(summary=_("Relative Wealth Indexes Vector Tiles")),
    download=extend_schema(summary=_("Relative Wealth Indexes CSV")),
)
class RelativeWealthIndexViewSet(CSVDownloadMixin, VectorLayer, ReadOnlyModelViewSet):
    """
    A ViewSet for managing :class:`demographics.models.RelativeWealthIndex` objects.

    This viewset provides endpoints for:

    - Listing all relative wealth indexes (`list` endpoint).
    - Retrieving a specific relative wealth index by UUID (`retrieve` endpoint).
    - Export relative wealth indexes to a `CSV` file (`download` endpoint).
    - Provides Mapbox Vector Tiles (`mvt`) for relative wealth indexes (`tiles` endpoint).
    """

    #: A serializer class for converting `RelativeWealthIndex` objects to GeoJSON format.
    serializer_class: Type[RelativeWealthIndexSerializer] = RelativeWealthIndexSerializer

    #: A serializer class for converting `RelativeWealthIndex` objects to CSV format.
    csv_serializer_class: Type[RelativeWealthIndexCSVSerializer] = RelativeWealthIndexCSVSerializer

    #: A pagination class to handle GeoJSON format pagination for `RelativeWealthIndex` objects.
    pagination_class: Type[GeoJsonPagination] = GeoJsonPagination

    #: A lookup field used to retrieve a specific `RelativeWealthIndex` object.
    lookup_field: str = "uuid"

    #: A list of required OAuth2 scopes for accessing the `RelativeWealthIndex` API endpoints.
    required_scopes: List[str] = ["default"]

    #: A list of filter backends for applying search and order filters
    #: to the queryset of `RelativeWealthIndex` objects.
    filter_backends: List[Type[BaseFilterBackend]] = [
        DjangoFilterBackend,
        OrderingFilter,
        InBBoxFilter,
        TMSTileFilter,
        DistanceToPointFilter,
    ]

    #: A custom filter for applying complex filters to the queryset of
    #: `RelativeWealthIndex` objects.
    filterset_class: Type[RelativeWealthIndexFilter] = RelativeWealthIndexFilter

    #: A list of fields that are used for ordering the queryset of
    #: `RelativeWealthIndex` objects (e.g., `?ordering=<field>`).
    ordering_fields: List[str] = ["rwi", "error", "created_at", "updated_at"]

    #: A `RelativeWealthIndex` geometry field used in performing bounding box filtering
    #: on the queryset of `RelativeWealthIndex` objects via query parameters
    #: (i.e., `?in_bbox=<bbox>`).
    bbox_filter_field: str = "geometry"

    #: Whether to include `RelativeWealthIndex` objects that overlap the bounding box
    #: on the queryset.
    bbox_filter_include_overlapping: bool = False

    #: A `RelativeWealthIndex` geometry field used in filtering queryset of `RelativeWealthIndex`
    #: objects based on their distance from a specific point via query
    #: parameters (i.e., `?point=<x,y>&radius=<distance>`).
    distance_filter_field: str = "geometry"

    #: Whether to convert the distance value to meters before filtering
    #: queryset of `RelativeWealthIndex` objects based on their distance from a
    #: specific point
    distance_filter_convert_meters: bool = True

    #: A default queryset for retrieving `RelativeWealthIndex` objects.
    queryset: QuerySet[RelativeWealthIndex] = (
        RelativeWealthIndex.objects.select_related("administrative_area").order_by("-created_at").all()
    )

    #: Vector tiles layer ID
    id = "relative-wealth-index"

    #: A tuple of fields to be included in vector tiles data.
    tile_fields = (
        "rwi",
        "error",
        "country",
        "administrative_area_uuid",
        "administrative_area_name",
    )
    tile_buffer = 64

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
        name="Download Relative Wealth Indexes CSV",
        url_path="download",
        url_name="list-download",
    )
    def download(self, request, *args, **kwargs):
        """Download relative wealth indexes as CSV file."""

        return self.export_csv(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        name="Relative Wealth Indexes Vector Tiles",
        renderer_classes=(MVTRenderer,),
        url_path=r"tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).mvt",
        url_name="tile",
    )
    @method_decorator(cache_page(MVT_CACHE_TIMEOUT, key_prefix="mvt:relative-wealth-index", cache=MVT_CACHE_ALIAS))
    def tile(self, request, *args, **kwargs):
        """Provides Mapbox Vector Tiles for relative wealth indexes."""
        return Response(self.get_tile(x=int(kwargs.get("x")), y=int(kwargs.get("y")), z=int(kwargs.get("z"))))
