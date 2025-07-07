from typing import List, Type

from rest_framework import serializers

from administrative.api.serializers import RelatedAreaSerializer

from ..models import ExposureCoverage, HazardExposure

__all__ = ["ExposureCoverageSerializer", "HazardExposureSerializer"]


class ExposureCoverageSerializer(serializers.ModelSerializer):
    """A ModelSerializer for serializing :class:`hazards.models.ExposureCoverage` model."""

    administrative_area = RelatedAreaSerializer(read_only=True)
    tms_url = serializers.CharField(read_only=True)

    class Meta:
        """Metadata for the :class:`ExposureCoverageSerializer`.

        Attributes:
            model (Type[ExposureCoverage]):
                The model class that this serializer represents.

            exclude (List[str]):
                A list of fields to exclude from the serialized output.
        """

        model: Type[ExposureCoverage] = ExposureCoverage
        exclude: List[str] = ["id", "raster"]


class HazardExposureSerializer(serializers.ModelSerializer):
    """A ModelSerializer for serializing :class:`hazards.models.HazardExposure` model."""

    country = RelatedAreaSerializer(source="coverage.administrative_area", read_only=True)
    administrative_area_name = serializers.CharField(source="coverage.administrative_area.name", read_only=True)
    urbanization_degree_name = serializers.CharField(source="urbanization_degree.name", read_only=True)

    class Meta:
        """Metadata for the :class:`HazardExposureSerializer`.

        Attributes:
            model (Type[HazardExposure]):
                The model class that this serializer represents.

            fields (List[str]):
                A list of fields to be included in the serialized output.

            read_only_fields (List[str]):
                A list of fields that cannot be modified during updates.
        """

        model: Type[HazardExposure] = HazardExposure
        fields = [
            "uuid",
            "hazards_names_display",
            "administrative_area_name",
            "urbanization_degree_name",
            "country",
            "population_exposed",
            "population_exposed_percent",
            "population_exposed_ev",
            "population_exposed_ev_percent",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
