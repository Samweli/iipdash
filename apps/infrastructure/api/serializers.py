from typing import List, Type

from rest_framework_gis import serializers

from administrative.api.serializers import RelatedAreaSerializer
from infrastructure.models import CellTower, FiberOptic

__all__ = ["CellTowerSerializer", "FiberOpticSerializer"]


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


class FiberOpticSerializer(serializers.GeoFeatureModelSerializer):
    """A fiber optic network."""

    #: Nested serializer for the related administrative area
    administrative_area = RelatedAreaSerializer(read_only=True)

    class Meta:
        """Metadata for the :class:`FiberOpticSerializer`.

        Attributes:
            model (Type[FiberOptic]):
                The model class that this serializer represents.

            id_field (str):
                A field in the model used as the GeoJSON `id` property.

            geo_field (str):
                A field in the model representing the geospatial geometry.

            exclude (List[str]):
                A list of fields to exclude from the serialized output.
        """

        model: Type[FiberOptic] = FiberOptic
        id_field: str = "uuid"
        geo_field: str = "geometry"
        exclude: List[str] = ["id"]
