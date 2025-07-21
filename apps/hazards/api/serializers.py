from typing import List, Type

from rest_framework import serializers

from administrative.api.serializers import RelatedAreaSerializer

from ..models import ExposureCoverage, HazardExposure, UrbanizationDegree

__all__ = ["ExposureCoverageSerializer", "HazardExposureSerializer", "RelatedUrbanizationDegreeSerializer"]


class RelatedUrbanizationDegreeSerializer(serializers.ModelSerializer):
    """A related urbanization degree serializer."""

    class Meta:
        model = UrbanizationDegree
        fields = ["uuid", "name", "code", "group"]


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

    administrative_area = RelatedAreaSerializer(source="coverage.administrative_area", read_only=True)
    urbanization_degree = RelatedUrbanizationDegreeSerializer(read_only=True)

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
            "administrative_area",
            "urbanization_degree",
            "population_exposed",
            "population_exposed_percent",
            "population_exposed_ev",
            "population_exposed_ev_percent",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
