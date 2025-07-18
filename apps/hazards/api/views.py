from typing import List, Type

from django.conf import settings
from django.db.models import ExpressionWrapper, F, FloatField, QuerySet, Sum
from django.db.models.functions import Coalesce, NullIf
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import ExposureCoverage, HazardExposure
from .filters import ExposureCoverageFilter, HazardExposureFilter
from .serializers import ExposureCoverageSerializer, HazardExposureSerializer

__all__ = ["ExposureCoverageViewSet", "HazardExposureViewSet"]

MVT_CACHE_ALIAS = settings.CACHE_MVT_ALIAS
MVT_CACHE_TIMEOUT = settings.CACHE_TIMEOUTS["mvt"]


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
    aggregates=extend_schema(summary=_("Hazards Exposure Aggregates")),
)
class HazardExposureViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for managing :class:`hazards.models.HazardExposure` objects.

    This viewset provides endpoints for:

    - Listing all hazards exposures (`list` endpoint).
    - Retrieving a specific hazards exposure by UUID (`retrieve` endpoint).
    - Retrieving aggregates summary for hazards exposures (`aggregates` endpoint).
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

    @action(
        detail=False,
        methods=["get"],
        name="Summary statistics related to hazards exposure.",
        url_path="aggregates",
        url_name="aggregates",
    )
    def aggregates(self, request, *args, **kwargs):
        """Returns summary statistics related to hazards exposure."""
        base_queryset = self.filter_queryset(self.get_queryset())

        data = (
            base_queryset.values("coverage__administrative_area_id")
            .annotate(
                area_population=F("coverage__administrative_area__population"),
                area_population_exposed=Coalesce(Sum("population_exposed"), 0),
                area_population_exposed_ev=Coalesce(Sum("population_exposed_ev"), 0),
            )
            .order_by("coverage__administrative_area_id")
            .aggregate(
                population=Sum("area_population"),
                population_exposed=Sum("area_population_exposed"),
                population_exposed_ev=Sum("area_population_exposed_ev"),
                population_exposed_percent=ExpressionWrapper(
                    F("population_exposed") * 100 / NullIf(F("population"), 0),
                    output_field=FloatField(),
                ),
                population_exposed_ev_percent=ExpressionWrapper(
                    F("population_exposed_ev") * 100 / NullIf(F("population"), 0),
                    output_field=FloatField(),
                ),
            )
        )

        return Response(data, status=status.HTTP_200_OK)
