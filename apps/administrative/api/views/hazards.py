from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F, IntegerField, OuterRef, Subquery, Sum, Value
from django.db.models.functions import Coalesce
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.fields import BooleanField
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.pagination import GeoJsonPagination
from vectortiles.backends.postgis import VectorLayer

from hazards.models import HazardExposure

from ..filters import AreaHazardExposureFilter, AreaHazardExposureFilter2
from ..serializers import AreaHazardExposureSerializer, AreaHazardExposureSerializer2, AreaHazardExpsoureCSVSerializer
from .base import AreaViewSet

__all__ = ["AreaHazardExposureViewSet", "AreaHazardExposureViewSet2"]


@extend_schema_view(
    list=extend_schema(
        summary=_("Administrative Areas Hazard Exposure"),
        description=_("Retrieve a list of administrative areas with hazard exposure statistics."),
    ),
    retrieve=extend_schema(
        summary=_("Administrative Area Hazard Exposure"),
        description=_("Retrieve details of an administrative area with hazard exposure statistics."),
    ),
)
class AreaHazardExposureViewSet(AreaViewSet):
    """Hazard Exposure summary for Administrative Areas API endpoint."""

    serializer_class = AreaHazardExposureSerializer
    csv_serializer_class = AreaHazardExpsoureCSVSerializer

    ordering_fields = ["name", "created_at", "updated_at"]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AreaHazardExposureFilter

    def get_queryset(self):
        """
        Returns a queryset of administrative areas annotated with hazard exposure data.

        This method:

        - Filter first the queryset using the request parameters
          via the `filterset_class` to ensure that only relevant data is considered before any annotation
          or aggregation.

        - The `population_exposed` and `population_exposed_ev`
          annotations use `Subquery` to perform accurate aggregation of hazard exposure values per
          administrative area.
          This avoids inflated results due to duplicate joins across related models.

        - Applies `.distinct()` to the queryset to avoid duplicate administrative areas in the
         API response when multiple hazard exposures exist.

        Returns:
            QuerySet: A queryset of administrative areas with annotated hazard exposure data.
        """
        qs = super().get_queryset()

        query_params = self.request.GET.copy()
        if "hazard_type" in query_params:
            query_params.setlist("hazards__code", query_params.getlist("hazard_type"))

        if "urbanization_degree" in query_params:
            query_params.setlist("urbanization_degree__code", query_params.getlist("urbanization_degree"))

        filterset = self.filterset_class(query_params, queryset=qs)
        qs = filterset.qs

        hazard_codes = query_params.getlist("hazards__code")
        urban_codes = query_params.getlist("urbanization_degree__code")

        hazard_qs = HazardExposure.objects.filter(coverage__administrative_area=OuterRef("pk"))
        hazard_ev_qs = HazardExposure.objects.filter(coverage__administrative_area=OuterRef("pk"))

        if hazard_codes:
            hazard_qs = hazard_qs.filter(hazards__code__in=hazard_codes)
            hazard_ev_qs = hazard_ev_qs.filter(hazards__code__in=hazard_codes)
        if urban_codes:
            hazard_qs = hazard_qs.filter(urbanization_degree__code__in=urban_codes)
            hazard_ev_qs = hazard_ev_qs.filter(urbanization_degree__code__in=urban_codes)

        hazard_qs = (
            hazard_qs.values("coverage__administrative_area")
            .annotate(total_exposed=Sum("population_exposed"))
            .values("total_exposed")[:1]
        )

        hazard_ev_qs = (
            hazard_ev_qs.values("coverage__administrative_area")
            .annotate(total_exposed_ev=Sum("population_exposed_ev"))
            .values("total_exposed_ev")[:1]
        )

        qs = (
            qs.annotate(
                population_exposed=Coalesce(Subquery(hazard_qs, output_field=IntegerField()), Value(0)),
                population_exposed_ev=Coalesce(Subquery(hazard_ev_qs, output_field=IntegerField()), Value(0)),
                urbanization_degree_codes=ArrayAgg(
                    "hazards_exposure_coverage__exposure__urbanization_degree__code", distinct=True
                ),
                hazard_codes=ArrayAgg("hazards_exposure_coverage__exposure__hazards__code", distinct=True),
            )
            .order_by("id", "name")
            .distinct()
        )

        return qs

    def get_csv_file_name(self):
        """Return name of the CSV file produced."""
        return f"areas-hazards-exposure-summary-{now().date()}.csv"

    @action(
        detail=False,
        methods=["get"],
        name="Download areas hazards exposure statistics CSV",
        url_path="download",
        url_name="list-download",
    )
    def download(self, request, *args, **kwargs):
        """Download Areas Hazard Exposure Statistics as  aCSV."""

        return self.export_csv(request, *args, **kwargs)


class AreaHazardExposureViewSet2(VectorLayer, ReadOnlyModelViewSet):
    """Hazard Exposure summary for Administrative Areas API endpoint."""

    serializer_class = AreaHazardExposureSerializer2
    filterset_class = AreaHazardExposureFilter2
    pagination_class = GeoJsonPagination
    required_scopes = ["default"]

    def get_serializer(self, *args, **kwargs):

        # Optionally exclude geometry values in the response.
        exclude_geometry = self.request.query_params.get("exclude_geometry", "")
        kwargs["exclude_geometry"] = exclude_geometry.lower() in BooleanField.TRUE_VALUES
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        qs = (
            HazardExposure.objects.values(administrative_area_uuid=F("coverage__administrative_area__uuid"))
            .annotate(
                country=F("coverage__administrative_area__country"),
                administrative_area_name=F("coverage__administrative_area__name"),
                administrative_area_depth=F("coverage__administrative_area__depth"),
                exposed_population=Sum("population_exposed"),
                ev_exposed_population=Sum("population_exposed_ev"),
                exposed_population_percent=Sum("population_exposed_percent"),
                ev_exposed_population_percent=Sum("population_exposed_ev_percent"),
                geom=F("coverage__administrative_area__geom"),
                population=F("coverage__administrative_area__population"),
            )
            .order_by("country", "administrative_area_name")
        )

        return qs
