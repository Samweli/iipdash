from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.db.models.functions import Cast
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.pagination import GeoJsonPagination
from vectortiles.backends.postgis import VectorLayer
from vectortiles.rest_framework.renderers import MVTRenderer

from ..models import HealthFacility
from .serializers import HealthFacilitySerializer

MVT_CACHE_ALIAS = settings.CACHE_MVT_ALIAS
MVT_CACHE_TIMEOUT = settings.CACHE_TIMEOUTS["mvt"]


class HealthFacilityViewSet(VectorLayer, ReadOnlyModelViewSet):
    """Relative wealth index API endpoint."""

    serializer_class = HealthFacilitySerializer
    lookup_field = "uuid"
    required_scopes = ["default"]
    pagination_class = GeoJsonPagination

    #: Vector tiles layer ID
    id = "health-facilities"

    #: A tuple of fields to be included in vector tiles data.
    tile_fields = (
        "name",
        "amenities",
        "osm_type",
        "osm_id",
    )

    queryset = HealthFacility.objects.order_by("-created_at")

    def get_vector_tile_queryset(self, *args, **kwargs):
        """Returns a queryset used to generate vector tiles."""
        queryset = self.get_queryset().annotate(geom=Cast("geometry", PointField()))
        queryset = self.filter_queryset(queryset)
        return queryset

    @action(
        detail=False,
        methods=["get"],
        renderer_classes=(MVTRenderer,),
        url_path=r"tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).mvt",
        url_name="tile",
    )
    @method_decorator(cache_page(MVT_CACHE_TIMEOUT, key_prefix="mvt:health-facilities", cache=MVT_CACHE_ALIAS))
    def tile(self, request, *args, **kwargs):
        """Provides Mapbox Vector Tiles."""
        return Response(self.get_tile(x=int(kwargs.get("x")), y=int(kwargs.get("y")), z=int(kwargs.get("z"))))
