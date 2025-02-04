from django.conf import settings
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.pagination import GeoJsonPagination
from vectortiles.backends.postgis import VectorLayer
from vectortiles.rest_framework.renderers import MVTRenderer

from core.api.mixins import CSVDownloadMixin

from ..models import Area
from .filters import AreaFilter
from .serializers import (
    AreaCSVSerializer,
    AreaEducationCSVSerializer,
    AreaEducationIFONDCSVSerializer,
    AreaEducationIFONDSerializer,
    AreaEducationSerializer,
    AreaSerializer,
)

__all__ = ["AreaViewSet", "AreaEducationViewSet", "AreaEducationIFONDViewSet"]


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
    @method_decorator(cache_page(MVT_CACHE_TIMEOUT))
    def tile(self, request, *args, **kwargs):
        """Provides Mapbox Vector Tiles for administrative areas."""
        return Response(self.get_tile(x=int(kwargs.get("x")), y=int(kwargs.get("y")), z=int(kwargs.get("z"))))


@extend_schema_view(
    list=extend_schema(
        summary=_("Administrative Areas Education Statistics"),
        description=_("Retrieve a list of administrative areas with education statistics."),
    ),
    retrieve=extend_schema(
        summary=_("Administrative Area Education Statistics"),
        description=_("Retrieve details of an administrative area with education statistics."),
    ),
    download=extend_schema(summary=_("Administrative Areas Education Statistics CSV")),
    tile=extend_schema(summary=_("Administrative Areas Education Statistics Vector Tiles")),
)
class AreaEducationViewSet(AreaViewSet):
    """Education Summary for an Administrative Area API endpoint."""

    serializer_class = AreaEducationSerializer
    ordering_fields = ["name", "created_at", "updated_at"]
    csv_serializer_class = AreaEducationCSVSerializer

    #: Vector tiles layer ID
    id = "areas-education"

    #: A tuple of fields to be included in vector tiles data.
    tile_fields = (
        "uuid",
        "type_code",
        "country",
        "name",
        "code",
        "description",
        "institutions_count",
        "institutions_electrified",
        "institutions_fiber_connected",
        "institutions_electrified_no_fiber",
        "institutions_fiber_10km",
        "institutions_fiber_15km",
        "institutions_fiber_20km",
    )

    def get_queryset(self):

        qs = Area.objects.annotate(
            institutions_count=Count("related_education_institution"),
            institutions_electrified=Count(
                "related_education_institution", filter=Q(related_education_institution__has_electricity=True)
            ),
            institutions_fiber_connected=Count(
                "related_education_institution", filter=Q(related_education_institution__has_fiber_optic=True)
            ),
            institutions_electrified_no_fiber=Count(
                "related_education_institution",
                filter=Q(
                    related_education_institution__has_electricity=True,
                    related_education_institution__has_fiber_optic=False,
                ),
            ),
            institutions_fiber_10km=Count(
                "related_education_institution",
                filter=Q(related_education_institution__fon_distance__lte=10000),
            ),
            institutions_fiber_15km=Count(
                "related_education_institution",
                filter=Q(related_education_institution__fon_distance__lte=15000),
            ),
            institutions_fiber_20km=Count(
                "related_education_institution",
                filter=Q(related_education_institution__fon_distance__lte=20000),
            ),
        )

        return qs

    def get_vector_tile_queryset(self, *args, **kwargs):
        """Returns a queryset used to generate vector tiles."""

        queryset = self.get_queryset().order_by()
        queryset = self.filter_queryset(queryset)

        return queryset

    @action(
        detail=False,
        methods=["get"],
        name="Download Areas Education Statistics CSV",
        url_path="download",
        url_name="list-download",
    )
    def download(self, request, *args, **kwargs):
        """Download Areas Education Statistics as CSV."""

        return self.export_csv(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        renderer_classes=(MVTRenderer,),
        url_path=r"tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).mvt",
        url_name="tile",
    )
    @method_decorator(cache_page(MVT_CACHE_TIMEOUT))
    def tile(self, request, *args, **kwargs):
        """Provides Mapbox Vector Tiles for administrative areas with education statistics"""
        return Response(self.get_tile(x=int(kwargs.get("x")), y=int(kwargs.get("y")), z=int(kwargs.get("z"))))


@extend_schema_view(
    list=extend_schema(
        summary=_("Administrative Areas and Education Institutions Fiber Distance"),
        description=_(
            "Summary Education Institutions within specified distance to "
            "fiber optic nodes within administrative areas."
        ),
    ),
    retrieve=extend_schema(
        summary=_("Administrative Area Education and Fiber Distance"),
        description=_(
            "Summary number of Education Institutions within specified "
            "distance to fiber optic nodes within a specific administrative areas."
        ),
    ),
    download=extend_schema(summary=_("Administrative Area Education and Fiber Distance CSV")),
    tile=extend_schema(summary=_("Administrative Area Education and Fiber Distance Vector Tiles")),
)
class AreaEducationIFONDViewSet(AreaViewSet):
    """Summarization of Number of Education Institutions within specified distance to a fiber optic node
    within Administrative Areas."""

    serializer_class = AreaEducationIFONDSerializer
    ordering_fields = ["name", "created_at", "updated_at"]
    csv_serializer_class = AreaEducationIFONDCSVSerializer

    #: Vector tiles layer ID
    id = "areas-education-ifond"

    #: A tuple of fields to be included in vector tiles data.
    tile_fields = (
        "uuid",
        "type_code",
        "country",
        "name",
        "code",
        "description",
        "institutions_count",
        "institutions_electrified",
        "institutions_fiber_connected",
        "institutions_electrified_no_fiber",
    )

    def clean_distance(self):
        error_message = _("Invalid distance value")

        distance = self.kwargs["distance"]

        try:
            distance = int(distance)
        except (ValueError, TypeError):
            raise ParseError(detail=error_message)

        if distance < 0:
            raise ParseError(detail=error_message)

        return distance

    def get_queryset(self):

        distance = self.clean_distance()

        qs = Area.objects.annotate(
            # all institutions within distance
            institutions_count=Count(
                "related_education_institution",
                filter=Q(related_education_institution__fon_distance__lte=distance),
            ),
            # institutions within distance connected to electricity
            institutions_electrified=Count(
                "related_education_institution",
                filter=Q(related_education_institution__has_electricity=True)
                & Q(related_education_institution__fon_distance__lte=distance),
            ),
            # institutions within distance connected to fiber
            institutions_fiber_connected=Count(
                "related_education_institution",
                filter=Q(related_education_institution__has_fiber_optic=True)
                & Q(related_education_institution__fon_distance__lte=distance),
            ),
            # institutions within distance connected to electricity but not to fiber
            institutions_electrified_no_fiber=Count(
                "related_education_institution",
                filter=Q(
                    related_education_institution__has_electricity=True,
                    related_education_institution__has_fiber_optic=False,
                )
                & Q(related_education_institution__fon_distance__lte=distance),
            ),
        )

        return qs

    def get_vector_tile_queryset(self, *args, **kwargs):
        """Returns a queryset used to generate vector tiles."""

        queryset = self.get_queryset().order_by()
        queryset = self.filter_queryset(queryset)

        return queryset

    @action(
        detail=False,
        methods=["get"],
        name="Download Areas Education Statistics CSV",
        url_path="download",
        url_name="list-download",
    )
    def download(self, request, *args, **kwargs):
        """Returns Summary number of Education Institutions within specified "
        distance to fiber optic nodes within a specific administrative areas as CSV file.
        """

        return self.export_csv(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        renderer_classes=(MVTRenderer,),
        url_path=r"tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).mvt",
        url_name="tile",
    )
    @method_decorator(cache_page(MVT_CACHE_TIMEOUT))
    def tile(self, request, *args, **kwargs):
        """Provides Mapbox Vector Tiles for administrative areas with number of education institutions
        within the specified distance."""
        return Response(self.get_tile(x=int(kwargs.get("x")), y=int(kwargs.get("y")), z=int(kwargs.get("z"))))
