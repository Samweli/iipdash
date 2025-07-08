from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, Sum
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action

from ...models import Area
from ..filters import AreaHazardExposureFilter
from ..serializers import AreaHazardExposureSerializer, AreaHazardExpsoureCSVSerializer
from .base import AreaViewSet

__all__ = ["AreaHazardExposureViewSet"]


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
        qs = super().get_queryset()

        filterset = self.filterset_class(self.request.GET, queryset=qs)
        qs = filterset.qs

        qs = qs.annotate(
            population_exposed=Sum("hazards_exposure_coverage__exposure__population_exposed"),
            population_exposed_ev=Sum("hazards_exposure_coverage__exposure__population_exposed_ev"),
            urbanization_degree_codes=ArrayAgg(
                "hazards_exposure_coverage__exposure__urbanization_degree__code",
                distinct=True,
            ),
            hazard_codes=ArrayAgg(
                "hazards_exposure_coverage__exposure__hazards__code",
                distinct=True,
            ),
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
