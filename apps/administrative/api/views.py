from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.renderers import JSONRenderer
from rest_framework_gis.pagination import GeoJsonPagination

from ..models import Area
from .filters import AreaFilter
from .serializer import AreaEducationSerializer, AreaSerializer

__all__ = ["AreaViewSet"]


@extend_schema_view(
    list=extend_schema(
        summary=_("List Administrative Areas"),
        description=_("Retrieve a list of administrative areas."),
    ),
    retrieve=extend_schema(
        summary=_("Retrieve Administrative Area"),
        description=_("Retrieve details of an administrative area."),
    ),
)
class AreaViewSet(viewsets.ReadOnlyModelViewSet):
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

    queryset = Area.objects.all()


@extend_schema_view(
    list=extend_schema(
        summary=_("List Area Education Summary"),
        description=_("Retrieve a list of administrative areas."),
    ),
    retrieve=extend_schema(
        summary=_("Retrieve Area Education Summary"),
        description=_("Retrieve details of an administrative area."),
    ),
)
class AreaEducationViewSet(AreaViewSet):
    """Education Summary for an Administrative Area API endpoint."""

    serializer_class = AreaEducationSerializer
    ordering_fields = ["name", "created_at", "updated_at"]

    def get_queryset(self):

        qs = Area.objects.annotate(
            # institutions_count=Subquery(aggregates[:1]),
            institutions_count=Count("education_institution"),
            institutions_electrified=Count(
                "education_institution", filter=Q(education_institution__has_electricity=True)
            ),
            institutions_fiber_connected=Count(
                "education_institution", filter=Q(education_institution__has_fiber_optic=True)
            ),
            institutions_electrified_no_fiber=Count(
                "education_institution",
                filter=Q(education_institution__has_electricity=True, education_institution__has_fiber_optic=False),
            ),
            institutions_fiber_10km=Count(
                "education_institution",
                filter=Q(education_institution__fon_distance__lte=10000),
            ),
            institutions_fiber_15km=Count(
                "education_institution",
                filter=Q(education_institution__fon_distance__lte=15000),
            ),
            institutions_fiber_20km=Count(
                "education_institution",
                filter=Q(education_institution__fon_distance__lte=20000),
            ),
        )

        return qs
