from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.renderers import JSONRenderer
from rest_framework_gis.pagination import GeoJsonPagination

from ..models import Area
from .filters import AreaFilter
from .serializer import AreaSerializer

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
