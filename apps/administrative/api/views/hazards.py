from django.conf import settings
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, Sum
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view

from ...models import Area
from ..serializers import AreaHazardExposureSerializer
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
    ordering_fields = ["name", "created_at", "updated_at"]

    def get_queryset(self):

        qs = Area.objects.annotate(
            population_exposed=Sum("hazards_exposure_coverage__exposure__population_exposed"),
            population_exposed_ev=Sum("hazards_exposure_coverage__exposure__population_exposed_ev"),
            urbanization_degree_codes=ArrayAgg(
                "hazards_exposure_coverage__exposure__urbanization_degree__code",
                distinct=True,
                filter=~Q(hazards_exposure_coverage__exposure__urbanization_degree__code=None),
            ),
        )

        return qs
