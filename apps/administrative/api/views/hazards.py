from django.conf import settings
from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.fields import BooleanField
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.pagination import GeoJsonPagination
from vectortiles.backends.postgis import VectorLayer
from vectortiles.rest_framework.renderers import MVTRenderer

from core.api.mixins import CSVDownloadMixin
from hazards.models import HazardExposure

from ..filters import AreaHazardExposureFilter
from ..serializers import AreaHazardExposureCSVSerializer, AreaHazardExposureSerializer

__all__ = ["AreaHazardExposureViewSet"]


MVT_CACHE_ALIAS = settings.CACHE_MVT_ALIAS
MVT_CACHE_TIMEOUT = settings.CACHE_TIMEOUTS["mvt"]


@extend_schema_view(
    list=extend_schema(
        summary=_("Administrative Areas Hazards Exposure"),
        description=_("Retrieve a list of administrative areas with hazard exposure statistics."),
    ),
    retrieve=extend_schema(
        summary=_("Administrative Area Hazards Exposure"),
        description=_("Retrieve details of an administrative area with hazard exposure statistics."),
    ),
    download=extend_schema(summary=_("Administrative Area Hazards Exposure Summary CSV")),
    tile=extend_schema(summary=_("Administrative Area Hazards Exposure Vector Tiles")),
)
class AreaHazardExposureViewSet(CSVDownloadMixin, VectorLayer, ReadOnlyModelViewSet):
    """Hazard Exposure summary for Administrative Areas API endpoint."""

    serializer_class = AreaHazardExposureSerializer
    csv_serializer_class = AreaHazardExposureCSVSerializer
    filterset_class = AreaHazardExposureFilter
    pagination_class = GeoJsonPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [JSONRenderer]
    lookup_field = "administrative_area_uuid"
    required_scopes = ["default"]

    #: Vector tiles layer ID
    id = "areas-hazards-exposure"

    #: A tuple of fields to be included in vector tiles data.
    tile_fields = (
        "administrative_area_uuid",
        "country",
        "name",
        "depth",
        "population_weighted_rwi",
        "exposed_population",
        "ev_exposed_population",
        "exposed_population_percent",
        "ev_exposed_population_percent",
        "population",
    )

    def get_serializer(self, *args, **kwargs):

        # Optionally exclude geometry values in the response.
        exclude_geometry = self.request.query_params.get("exclude_geometry", "")
        kwargs["exclude_geometry"] = exclude_geometry.lower() in BooleanField.TRUE_VALUES
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):

        aggregates_filter = self.get_aggregates_filter()

        qs = (
            HazardExposure.objects.values(administrative_area_uuid=F("coverage__administrative_area__uuid"))
            .annotate(
                country=F("coverage__administrative_area__country"),
                name=F("coverage__administrative_area__name"),
                depth=F("coverage__administrative_area__depth"),
                population_weighted_rwi=F("coverage__administrative_area__rwi_population_weighted"),
                exposed_population=Coalesce(Sum("population_exposed", filter=aggregates_filter), 0),
                ev_exposed_population=Coalesce(Sum("population_exposed_ev", filter=aggregates_filter), 0),
                exposed_population_percent=Coalesce(Sum("population_exposed_percent", filter=aggregates_filter), 0.0),
                ev_exposed_population_percent=Coalesce(
                    Sum("population_exposed_ev_percent", filter=aggregates_filter), 0.0
                ),
                population=F("coverage__administrative_area__population"),
                geom=F("coverage__administrative_area__geom"),
            )
            .order_by("country", "name")
        )

        return qs

    def get_aggregates_filter(self):
        filterset = self.filterset_class(data=self.request.query_params)
        return filterset.get_aggregates_filter()

    def get_csv_file_name(self):
        """Return name of the CSV file produced."""
        return f"areas-hazards-exposure-{now().date()}.csv"

    @action(
        detail=False,
        methods=["get"],
        name="Download Areas Hazards Exposure Statistics CSV",
        url_path="download",
        url_name="list-download",
    )
    def download(self, request, *args, **kwargs):
        """Download Areas Hazard Exposure Statistics as  aCSV."""
        return self.export_csv(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        renderer_classes=(MVTRenderer,),
        url_path=r"tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).mvt",
        url_name="tile",
    )
    @method_decorator(cache_page(MVT_CACHE_TIMEOUT, key_prefix="mvt:areas-hazards-exposure", cache=MVT_CACHE_ALIAS))
    def tile(self, request, *args, **kwargs):
        """Provides Mapbox Vector Tiles for administrative areas with hazards exposure statistics."""
        return Response(self.get_tile(x=int(kwargs.get("x")), y=int(kwargs.get("y")), z=int(kwargs.get("z"))))
