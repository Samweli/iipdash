from typing import List, Type

from rest_framework import serializers

from administrative.api.serializers import RelatedAreaSerializer

from ..models import ExposureCoverage

__all__ = ["ExposureCoverageSerializer"]


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
