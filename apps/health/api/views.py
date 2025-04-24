from typing import List, Type

from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.db.models import F
from django.db.models.functions import Cast
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.filters import BaseFilterBackend, OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.pagination import GeoJsonPagination
from vectortiles.backends.postgis import VectorLayer
from vectortiles.rest_framework.renderers import MVTRenderer

from core.api.filters import DistanceToPointFilter, InBBoxFilter, TMSTileFilter
from core.api.mixins import CSVDownloadMixin

from ..models import HealthFacility
from .serializers import HealthFacilityCSVSerializer, HealthFacilitySerializer

MVT_CACHE_ALIAS = settings.CACHE_MVT_ALIAS
MVT_CACHE_TIMEOUT = settings.CACHE_TIMEOUTS["mvt"]


@extend_schema_view(
    list=extend_schema(
        summary=_("Health Care Facilities"),
        description=_("Retrieve a list of health care facilities."),
    ),
    retrieve=extend_schema(
        summary=_("Health Care Facility"),
        description=_("Retrieve details of a specific health care facility."),
    ),
    tile=extend_schema(summary=_("Health Care Facility Vector Tiles")),
    download=extend_schema(summary=_("Health Care Facility CSV")),
)
class HealthFacilityViewSet(CSVDownloadMixin, VectorLayer, ReadOnlyModelViewSet):
    """Health Care Facility API endpoint"""

    serializer_class = HealthFacilitySerializer
    pagination_class = GeoJsonPagination
    lookup_field = "uuid"
    required_scopes = ["default"]
    permission_classes = [IsAuthenticatedOrReadOnly]

    #: A list of filter backends for applying search and order filters
    #: to the queryset of `HealthFacility` objects.
    filter_backends: List[Type[BaseFilterBackend]] = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
        InBBoxFilter,
        TMSTileFilter,
        DistanceToPointFilter,
    ]

    filter_fields = ["amenity", "osm_type", "administrative_area"]

    #: A `HealthFacility` geometry field used in performing bounding box filtering
    #: on the queryset of `HealthFacility` objects via query parameters
    #: (i.e., `?in_bbox=<bbox>`).
    bbox_filter_field: str = "geometry"
    bbox_filter_include_overlapping: bool = False

    #: A `HealthFacility` geometry field used in filtering queryset of `HealthFacility`
    #: objects based on their distance from a specific point via query
    #: parameters (i.e., `?point=<x,y>&radius=<distance>`).
    distance_filter_field = "geometry"
    distance_filter_convert_meters = True

    queryset = HealthFacility.objects.select_related("administrative_area").order_by("-created_at")

    csv_serializer_class = HealthFacilityCSVSerializer

    #: Vector tiles layer ID
    id = "health-facilities"

    #: A tuple of fields to be included in vector tiles data.
    tile_fields = (
        "uuid",
        "name",
        "amenity",
        "osm_id",
        "osm_type",
        "country",
        "administrative_area_uuid",
        "administrative_area_name",
    )

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
        name="Download health care facilities CSV",
        url_path="download",
        url_name="list-download",
    )
    def download(self, request, *args, **kwargs):
        """Download health care facilities as CSV file."""

        return self.export_csv(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        renderer_classes=(MVTRenderer,),
        url_path=r"tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).mvt",
        url_name="tile",
    )
    @method_decorator(cache_page(MVT_CACHE_TIMEOUT, key_prefix="mvt:health-facilities", cache=MVT_CACHE_ALIAS))
    def tile(self, request, *args, **kwargs):
        """Provides Mapbox Vector Tiles for health care facilities."""
        return Response(self.get_tile(x=int(kwargs.get("x")), y=int(kwargs.get("y")), z=int(kwargs.get("z"))))
