from typing import List, Type

from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from ..models import ExposureCoverage, HazardExposure
from .filters import ExposureCoverageFilter, HazardExposureFilter
from .serializers import ExposureCoverageSerializer, HazardExposureSerializer

__all__ = ["ExposureCoverageViewSet", "HazardExposureViewSet"]


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


@extend_schema_view(
    list=extend_schema(
        summary=_("Hazards Exposures"),
        description=_(
            "Retrieve a list of hazards exposures, with optional searching, filtering, ordering and pagination."
        ),
    ),
    retrieve=extend_schema(
        summary=_("Hazards Exposure"),
        description=_("Retrieve details of a specific hazards exposure."),
    ),
)
class HazardExposureViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for managing :class:`hazards.models.HazardExposure` objects.

    This viewset provides endpoints for:

    - Listing all hazards exposures (`list` endpoint).
    - Retrieving a specific hazards exposure by UUID (`retrieve` endpoint).
    - Export hazards exposures to a `CSV` file (`download` endpoint).
    - Provides Mapbox Vector Tiles (`mvt`) for hazards exposures (`tiles` endpoint).
    """

    #: A serializer class for converting `HazardExposure` objects to GeoJSON format.
    serializer_class: Type[HazardExposureSerializer] = HazardExposureSerializer

    #: A lookup field used to retrieve a specific `HazardExposure` object.
    lookup_field: str = "uuid"

    #: A list of required OAuth2 scopes for accessing the `HazardExposure` API endpoints.
    required_scopes: List[str] = ["default"]

    #: A custom filter for applying complex filters to the queryset of
    #: `HazardExposure` objects.
    filterset_class: Type[HazardExposureFilter] = HazardExposureFilter

    #: A default queryset for retrieving `HazardExposure` objects.
    queryset: QuerySet[HazardExposure] = HazardExposure.objects.prefetch_related(
        "coverage", "urbanization_degree", "hazards"
    ).order_by("-created_at")
