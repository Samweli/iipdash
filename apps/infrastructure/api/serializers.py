from typing import List, Type

from rest_framework_gis import serializers

from administrative.models import Area
from infrastructure.models import CellTower

__all__ = ["CellTowerSerializer"]


class RelatedAreaSerializer(serializers.ModelSerializer):
    """A related administrative area."""

    class Meta:
        """Metadata for the :class:`RelatedAreaSerializer`.

        Attributes:
            model (Type[Area]):
                The model class that this serializer represents.

            fields (List[str]):
                The list of fields to be included in the serialized data.
        """

        model: Type[Area] = Area
        fields: List[str] = ["uuid", "name", "country"]


class CellTowerSerializer(serializers.GeoFeatureModelSerializer):
    """A cellular tower."""

    #: Nested serializer for the related administrative area
    administrative_area = RelatedAreaSerializer(read_only=True)

    class Meta:
        """Metadata for the :class:`CellTowerSerializer`.

        Attributes:
            model (Type[CellTower]):
                The model class that this serializer represents.

            id_field (str):
                A field in the model used as the GeoJSON `id` property.

            geo_field (str):
                A field in the model representing the geospatial geometry.

            exclude (List[str]):
                A list of fields to exclude from the serialized output.
        """

        model: Type[CellTower] = CellTower
        id_field: str = "uuid"
        geo_field: str = "geometry"
        exclude: List[str] = ["id"]
