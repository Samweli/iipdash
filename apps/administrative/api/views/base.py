from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.fields import BooleanField
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.pagination import GeoJsonPagination
from vectortiles.backends.postgis import VectorLayer
from vectortiles.rest_framework.renderers import MVTRenderer

from core.api.mixins import CSVDownloadMixin

from ...models import Area
from ..filters import AreaFilter
from ..serializers import AreaCSVSerializer, AreaSerializer

__all__ = ["AreaViewSet"]


MVT_CACHE_ALIAS = settings.CACHE_MVT_ALIAS
MVT_CACHE_TIMEOUT = settings.CACHE_TIMEOUTS["mvt"]


@extend_schema_view(
    list=extend_schema(
        summary=_("Administrative Areas"),
        description=_("Retrieve a list of administrative areas."),
    ),
    retrieve=extend_schema(
        summary=_("Administrative Area"),
        description=_("Retrieve details of an administrative area."),
    ),
    download=extend_schema(summary=_("Administrative Areas CSV")),
    tile=extend_schema(summary=_("Administrative Areas Vector Tiles")),
)
class AreaViewSet(CSVDownloadMixin, VectorLayer, ReadOnlyModelViewSet):
    """Administrative Area API endpoint."""

    serializer_class = AreaSerializer
    lookup_field = "uuid"
    required_scopes = ["default"]
    permission_classes = [IsAuthenticatedOrReadOnly]

    pagination_class = GeoJsonPagination
    renderer_classes = [JSONRenderer]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AreaFilter
    search_fields = ["name"]
    ordering_fields = ["name", "created_at", "updated_at"]

    csv_serializer_class = AreaCSVSerializer

    #: Vector tiles layer ID
    id = "administrative-areas"

    #: A tuple of fields to be included in vector tiles data.
    tile_fields = (
        "uuid",
        "type_code",
        "country",
        "name",
        "code",
        "description",
        "area",
        "population",
        "population_year",
    )

    queryset = Area.objects.all()

    def get_vector_tile_queryset(self, *args, **kwargs):
        """Returns a queryset used to generate vector tiles."""

        queryset = self.get_queryset().order_by()
        queryset = self.filter_queryset(queryset)

        return queryset

    def get_serializer(self, *args, **kwargs):

        # Optionally exclude geometry values in the response.
        exclude_geometry = self.request.query_params.get("exclude_geometry", "")
        kwargs["exclude_geometry"] = exclude_geometry.lower() in BooleanField.TRUE_VALUES
        return super().get_serializer(*args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        name="Download Administrative Areas CSV",
        url_path="download",
        url_name="list-download",
    )
    def download(self, request, *args, **kwargs):
        """Returns Administrative Areas CSV"""
        return self.export_csv(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        renderer_classes=(MVTRenderer,),
        url_path=r"tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).mvt",
        url_name="tile",
    )
    @method_decorator(cache_page(MVT_CACHE_TIMEOUT, key_prefix="mvt:administrative-areas", cache=MVT_CACHE_ALIAS))
    def tile(self, request, *args, **kwargs):
        """Provides Mapbox Vector Tiles for administrative areas."""
        return Response(self.get_tile(x=int(kwargs.get("x")), y=int(kwargs.get("y")), z=int(kwargs.get("z"))))
