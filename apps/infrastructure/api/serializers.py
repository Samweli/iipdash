from typing import List, Type

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from administrative.api.serializers import RelatedAreaSerializer

from ..models import CellTower, ElectricityNetwork, FiberOptic, FiberOpticNode, MobileCoverage, NetworkGeneration

__all__ = [
    "NetworkGenerationSerializer",
    "RelatedNetworkGenerationSerializer",
    "CellTowerSerializer",
    "CellTowerCSVSerializer",
    "MobileCoverageSerializer",
    "FiberOpticSerializer",
    "FiberOpticCSVSerializer",
    "FiberOpticNodeSerializer",
    "FiberOpticNodeCSVSerializer",
    "ElectricityNetworkSerializer",
    "ElectricityNetworkCSVSerializer",
]


class NetworkGenerationSerializer(serializers.ModelSerializer):
    """mobile network generation"""

    class Meta:
        model = NetworkGeneration
        exclude = ["id"]


class RelatedNetworkGenerationSerializer(serializers.ModelSerializer):
    """mobile network generation"""

    class Meta:
        model = NetworkGeneration
        fields = ["uuid", "name", "code"]


class CellTowerSerializer(GeoFeatureModelSerializer):
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


class CellTowerCSVSerializer(serializers.ModelSerializer):

    country = serializers.CharField(source="administrative_area.country", read_only=True)
    administrative_area_name = serializers.CharField(source="administrative_area.name", read_only=True)
    geometry = serializers.CharField()

    class Meta:
        model = CellTower
        fields = [
            "uuid",
            "network_type",
            "mcc",
            "location_is_approximate",
            "range",
            "country",
            "administrative_area_name",
            "src_created_at",
            "src_created_at",
            "created_at",
            "updated_at",
            "geometry",
        ]

        # There might be some performance gains in making fields read only
        # https://hakibenita.com/django-rest-framework-slow#read-only-modelserializer
        read_only_fields = fields


class MobileCoverageSerializer(serializers.ModelSerializer):
    """Mobile Coverage serializer."""

    administrative_area = RelatedAreaSerializer(read_only=True)
    network_generation = RelatedNetworkGenerationSerializer(read_only=True)
    tms_url = serializers.CharField(read_only=True)

    class Meta:
        model = MobileCoverage
        exclude = ["id", "raster"]


class FiberOpticSerializer(GeoFeatureModelSerializer):
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


class FiberOpticCSVSerializer(serializers.ModelSerializer):
    """Fiber Optic Network CSV serializer."""

    country = serializers.CharField(source="administrative_area.country", read_only=True)
    administrative_area_name = serializers.CharField(source="administrative_area.name", read_only=True)
    geometry = serializers.CharField()

    class Meta:
        model = FiberOptic
        fields = [
            "uuid",
            "name",
            "status",
            "country",
            "administrative_area_name",
            "operator_name",
            "created_at",
            "updated_at",
            "geometry",
        ]

        # There might be some performance gains in making fields read only
        # https://hakibenita.com/django-rest-framework-slow#read-only-modelserializer
        read_only_fields = fields


class FiberOpticNodeSerializer(GeoFeatureModelSerializer):
    """Fiber Optic Node GeoJSON serializer."""

    administrative_area = RelatedAreaSerializer(read_only=True)

    class Meta:
        model = FiberOpticNode
        id_field = "uuid"
        geo_field = "geometry"
        exclude = ["id"]


class FiberOpticNodeCSVSerializer(serializers.ModelSerializer):
    """Fiber Optic Node CSV serializer."""

    country = serializers.CharField(source="administrative_area.country", read_only=True)
    administrative_area_name = serializers.CharField(source="administrative_area.name", read_only=True)
    geometry = serializers.CharField()

    class Meta:
        model = FiberOpticNode
        fields = [
            "uuid",
            "node_type",
            "country",
            "administrative_area_name",
            "created_at",
            "updated_at",
            "geometry",
        ]
        read_only_fields = fields


class ElectricityNetworkSerializer(GeoFeatureModelSerializer):
    administrative_area = RelatedAreaSerializer(read_only=True)

    class Meta:
        model = ElectricityNetwork
        id_field = "uuid"
        geo_field = "geometry"
        exclude = ["id"]


class ElectricityNetworkCSVSerializer(serializers.ModelSerializer):
    """Electricity Network CSV serializer."""

    country = serializers.CharField(source="administrative_area.country", read_only=True)
    administrative_area_name = serializers.CharField(source="administrative_area.name", read_only=True)
    geometry = serializers.CharField()

    class Meta:
        model = ElectricityNetwork
        fields = [
            "uuid",
            "voltage_kv",
            "status",
            "source",
            "from_nm",
            "to_nm",
            "network_type",
            "country",
            "administrative_area_name",
            "created_at",
            "updated_at",
            "geometry",
        ]
        read_only_fields = fields
