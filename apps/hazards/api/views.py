from typing import List, Type

from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from ..models import ExposureCoverage
from .filters import ExposureCoverageFilter
from .serializers import ExposureCoverageSerializer

__all__ = ["ExposureCoverageViewSet"]


@extend_schema_view(
    list=extend_schema(
        summary=_("Hazard Exposure Coverages"),
        description=_(
            "Retrieve a list of hazard exposure coverages, with optional searching, filtering, ordering and pagination."  # noqa
        ),
    ),
    retrieve=extend_schema(
        summary=_("Hazard Exposure Coverage"),
        description=_("Retrieve details of a specific hazard exposure coverage."),
    ),
)
class ExposureCoverageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for managing :class:`hazards.models.ExposureCoverage` objects.

    This viewset provides endpoints for:
    - Listing all hazard exposure coverages (`list` endpoint).
    - Retrieving a specific hazard exposure coverage by UUID (`retrieve` endpoint).
    """

    #: A serializer class for converting `ExposureCoverage` objects to GeoJSON format.
    serializer_class: Type[ExposureCoverageSerializer] = ExposureCoverageSerializer

    #: A lookup field used to retrieve a specific `ExposureCoverage` object.
    lookup_field: str = "uuid"

    #: A list of required OAuth2 scopes for accessing the `ExposureCoverage` API endpoints.
    required_scopes: List[str] = ["default"]

    #: A custom filter for applying complex filters to the queryset of
    #: `ExposureCoverage` objects.
    filterset_class: Type[ExposureCoverageFilter] = ExposureCoverageFilter

    #: A default queryset for retrieving `ExposureCoverage` objects.
    queryset: QuerySet[ExposureCoverage] = (
        ExposureCoverage.objects.defer("raster").select_related("administrative_area").order_by("administrative_area")
    )
