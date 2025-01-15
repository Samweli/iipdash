from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.exceptions import ParseError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.renderers import JSONRenderer
from rest_framework_gis.pagination import GeoJsonPagination

from ..models import Area
from .filters import AreaFilter
from .serializers import AreaEducationIFONDSerializer, AreaEducationSerializer, AreaSerializer

__all__ = ["AreaViewSet", "AreaEducationViewSet", "AreaEducationIFONDViewSet"]


@extend_schema_view(
    list=extend_schema(
        summary=_("List Administrative Areas"),
        description=_("Retrieve a list of administrative areas."),
    ),
    retrieve=extend_schema(
        summary=_("Retrieve an Administrative Area"),
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
        summary=_("List Areas and Education Statistics"),
        description=_("Retrieve a list of administrative areas with education statistics."),
    ),
    retrieve=extend_schema(
        summary=_("Retrieve an Area and Education Statistics"),
        description=_("Retrieve details of an administrative area with education statistics."),
    ),
)
class AreaEducationViewSet(AreaViewSet):
    """Education Summary for an Administrative Area API endpoint."""

    serializer_class = AreaEducationSerializer
    ordering_fields = ["name", "created_at", "updated_at"]

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


@extend_schema_view(
    list=extend_schema(
        summary=_("List Areas and Education Statistics based on fiber distance."),
        description=_(
            "This provides a summary of number of Education Institutions within specified "
            "distance to fiber optic nodes within administrative areas."
        ),
    ),
    retrieve=extend_schema(
        summary=_("Retrieve and Area and Education Statistics based on fiber distance."),
    ),
)
class AreaEducationIFONDViewSet(AreaViewSet):
    """Summarization of Number of Education Institutions within specified distance to a fiber optic node
    within Administrative Areas."""

    serializer_class = AreaEducationIFONDSerializer
    ordering_fields = ["name", "created_at", "updated_at"]

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
