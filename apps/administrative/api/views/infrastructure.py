from django.conf import settings
from django.db.models import Avg, Q, Sum
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.response import Response
from vectortiles.rest_framework.renderers import MVTRenderer

from ...models import Area
from ..serializers import (
    AreaInternetSpeedCSVSerializer,
    AreaInternetSpeedSerializer,
    AreaMobileCoverageCSVSerializer,
    AreaMobileCoverageSerializer,
)
from .base import AreaViewSet

__all__ = ["AreaMobileCoverageViewSet", "AreaInternetSpeedViewSet"]


MVT_CACHE_ALIAS = settings.CACHE_MVT_ALIAS
MVT_CACHE_TIMEOUT = settings.CACHE_TIMEOUTS["mvt"]


@extend_schema_view(
    list=extend_schema(
        summary=_("Administrative Areas Mobile Coverage"),
        description=_("Retrieve a list of administrative areas with mobile network coverage statistics."),
    ),
    retrieve=extend_schema(
        summary=_("Administrative Area Mobile Coverage"),
        description=_("Retrieve details of an administrative area with mobile network coverage statistics."),
    ),
    download=extend_schema(summary=_("Administrative Areas Mobile Coverage CSV")),
    tile=extend_schema(summary=_("Administrative Areas Mobile Coverage Vector Tiles")),
)
class AreaMobileCoverageViewSet(AreaViewSet):
    """Mobile Coverage summary for Administrative Areas API endpoint."""

    serializer_class = AreaMobileCoverageSerializer
    ordering_fields = ["name", "created_at", "updated_at"]

    csv_serializer_class = AreaMobileCoverageCSVSerializer

    #: Vector tiles layer ID
    id = "areas-mobile-coverage"

    #: A tuple of fields to be included in vector tiles data.
    tile_fields = (
        "uuid",
        "type_code",
        "country",
        "name",
        "code",
        "description",
        "population",
        "population_year",
        "population_density_hd_avg",
        "population_covered_2g",
        "population_covered_3g",
        "population_covered_4g",
        "population_covered_5g",
        "coverage_2g",
        "coverage_3g",
        "coverage_4g",
        "coverage_5g",
        "population_uncovered_2g",
        "population_uncovered_3g",
        "population_uncovered_4g",
        "population_uncovered_5g",
        "no_coverage_2g",
        "no_coverage_3g",
        "no_coverage_4g",
        "no_coverage_5g",
    )

    def get_queryset(self):

        qs = Area.objects.annotate(
            coverage_2g=Sum(
                "mobile_coverage__population_covered_percent",
                filter=Q(mobile_coverage__network_generation__code="2g"),
            ),
            coverage_3g=Sum(
                "mobile_coverage__population_covered_percent",
                filter=Q(mobile_coverage__network_generation__code="3g"),
            ),
            coverage_4g=Sum(
                "mobile_coverage__population_covered_percent",
                filter=Q(mobile_coverage__network_generation__code="4g"),
            ),
            coverage_5g=Sum(
                "mobile_coverage__population_covered_percent",
                filter=Q(mobile_coverage__network_generation__code="5g"),
            ),
            population_covered_2g=Sum(
                "mobile_coverage__population_covered",
                filter=Q(mobile_coverage__network_generation__code="2g"),
            ),
            population_covered_3g=Sum(
                "mobile_coverage__population_covered",
                filter=Q(mobile_coverage__network_generation__code="3g"),
            ),
            population_covered_4g=Sum(
                "mobile_coverage__population_covered",
                filter=Q(mobile_coverage__network_generation__code="4g"),
            ),
            population_covered_5g=Sum(
                "mobile_coverage__population_covered",
                filter=Q(mobile_coverage__network_generation__code="5g"),
            ),
            no_coverage_2g=Sum(
                "mobile_coverage__population_uncovered_percent",
                filter=Q(mobile_coverage__network_generation__code="2g"),
            ),
            no_coverage_3g=Sum(
                "mobile_coverage__population_uncovered_percent",
                filter=Q(mobile_coverage__network_generation__code="3g"),
            ),
            no_coverage_4g=Sum(
                "mobile_coverage__population_uncovered_percent",
                filter=Q(mobile_coverage__network_generation__code="4g"),
            ),
            no_coverage_5g=Sum(
                "mobile_coverage__population_uncovered_percent",
                filter=Q(mobile_coverage__network_generation__code="5g"),
            ),
            population_uncovered_2g=Sum(
                "mobile_coverage__population_uncovered",
                filter=Q(mobile_coverage__network_generation__code="2g"),
            ),
            population_uncovered_3g=Sum(
                "mobile_coverage__population_uncovered",
                filter=Q(mobile_coverage__network_generation__code="3g"),
            ),
            population_uncovered_4g=Sum(
                "mobile_coverage__population_uncovered",
                filter=Q(mobile_coverage__network_generation__code="4g"),
            ),
            population_uncovered_5g=Sum(
                "mobile_coverage__population_uncovered",
                filter=Q(mobile_coverage__network_generation__code="5g"),
            ),
        )

        return qs

    def get_csv_file_name(self):
        """Return name of the CSV file produced."""
        return f"areas-mobile-coverage-summary-{now().date()}.csv"

    @action(
        detail=False,
        methods=["get"],
        name="Download Areas Mobile Coverage Statistics CSV",
        url_path="download",
        url_name="list-download",
    )
    def download(self, request, *args, **kwargs):
        """Download Areas Mobile Coverage Statistics as CSV."""

        return self.export_csv(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        renderer_classes=(MVTRenderer,),
        url_path=r"tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).mvt",
        url_name="tile",
    )
    @method_decorator(cache_page(MVT_CACHE_TIMEOUT, key_prefix="mvt:areas-mobile-coverage", cache=MVT_CACHE_ALIAS))
    def tile(self, request, *args, **kwargs):
        """Provides Mapbox Vector Tiles for administrative areas with mobile coverage statistics"""
        return Response(self.get_tile(x=int(kwargs.get("x")), y=int(kwargs.get("y")), z=int(kwargs.get("z"))))


class AreaInternetSpeedViewSet(AreaViewSet):
    """Internet speed for Administrative Areas API endpoint."""

    serializer_class = AreaInternetSpeedSerializer
    csv_serializer_class = AreaInternetSpeedCSVSerializer
    ordering_fields = ["name", "created_at", "updated_at"]

    #: Vector tiles layer ID
    id = "areas-internet-speed"

    #: A tuple of fields to be included in vector tiles data.
    tile_fields = (
        "uuid",
        "type_code",
        "country",
        "name",
        "code",
        "fixed_speed",
        "mobile_speed",
    )

    def get_queryset(self):

        qs = Area.objects.annotate(
            fixed_speed=Avg("internet_speed__fixed_speed"),
            mobile_speed=Avg("internet_speed__mobile_speed"),
        )

        return qs

    @action(
        detail=False,
        methods=["get"],
        name="Download areas internet speed statistics CSV",
        url_path="download",
        url_name="list-download",
    )
    def download(self, request, *args, **kwargs):
        """Download Areas Internet Speed Statistics as CSV."""

        return self.export_csv(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        renderer_classes=(MVTRenderer,),
        url_path=r"tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).mvt",
        url_name="tile",
    )
    @method_decorator(cache_page(MVT_CACHE_TIMEOUT, key_prefix="mvt:areas-internet-speed", cache=MVT_CACHE_ALIAS))
    def tile(self, request, *args, **kwargs):
        """Provides Mapbox Vector Tiles for administrative areas with internet speed statistics"""
        return Response(self.get_tile(x=int(kwargs.get("x")), y=int(kwargs.get("y")), z=int(kwargs.get("z"))))
