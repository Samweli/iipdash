from django.conf import settings
from django.db.models import F
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.pagination import GeoJsonPagination
from vectortiles.backends.postgis import VectorLayer
from vectortiles.rest_framework.renderers import MVTRenderer

from ..models import PopulationDensityHD
from .filters import PopulationDensityHDFilter
from .serializers import PopulationDensityHDSerializer

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
