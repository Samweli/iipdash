from typing import List, Type

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from ..models import Area

__all__ = [
    "BaseAreaEducationSerializer",
    "BaseAreaEducationIFONDSerializer",
    "AreaSerializer",
    "AreaEducationSerializer",
    "AreaEducationCSVSerializer",
    "AreaEducationIFONDSerializer",
    "AreaEducationIFONDCSVSerializer",
    "RelatedAreaSerializer",
]


class BaseAreaEducationSerializer(serializers.ModelSerializer):
    """Base class for Education summary per administrative areas"""

    institutions_count = serializers.SerializerMethodField()
    institutions_electrified = serializers.SerializerMethodField()
    institutions_fiber_connected = serializers.SerializerMethodField()
    institutions_electrified_no_fiber = serializers.SerializerMethodField()
    institutions_fiber_10km = serializers.SerializerMethodField()
    institutions_fiber_15km = serializers.SerializerMethodField()
    institutions_fiber_20km = serializers.SerializerMethodField()

    def get_institutions_count(self, obj) -> int:
        """Number of education institutions."""
        return obj.institutions_count

    def get_institutions_electrified(self, obj) -> int:
        """Number of electrified education institutions"""
        return obj.institutions_electrified

    def get_institutions_fiber_connected(self, obj) -> int:
        """Number of education institutions connected to fiber optic."""
        return obj.institutions_fiber_connected

    def get_institutions_electrified_no_fiber(self, obj) -> int:
        """Number of electrified education institutions not connected to fiber optic."""
        return obj.institutions_electrified_no_fiber

    def get_institutions_fiber_10km(self, obj) -> int:
        """Number of education institutions with nearest fiber optic within 10km."""
        return obj.institutions_fiber_10km

    def get_institutions_fiber_15km(self, obj) -> int:
        """Number of education institutions with nearest fiber optic within 15km."""
        return obj.institutions_fiber_15km

    def get_institutions_fiber_20km(self, obj) -> int:
        """Number of education institutions with nearest fiber optic within 20km."""
        return obj.institutions_fiber_20km


class BaseAreaEducationIFONDSerializer(serializers.ModelSerializer):
    """Base serializer clas for summary education institutions statistics per administrative areas based on
    Fiber Optic Node/Network Distance."""

    institutions_count = serializers.SerializerMethodField()
    institutions_electrified = serializers.SerializerMethodField()
    institutions_fiber_connected = serializers.SerializerMethodField()
    institutions_electrified_no_fiber = serializers.SerializerMethodField()

    def get_institutions_count(self, obj) -> int:
        """Number of education institutions."""
        return obj.institutions_count

    def get_institutions_electrified(self, obj) -> int:
        """Number of electrified education institutions"""
        return obj.institutions_electrified

    def get_institutions_fiber_connected(self, obj) -> int:
        """Number of education institutions connected to fiber optic."""
        return obj.institutions_fiber_connected

    def get_institutions_electrified_no_fiber(self, obj) -> int:
        """Number of electrified education institutions not connected to fiber optic."""
        return obj.institutions_electrified_no_fiber


class AreaSerializer(GeoFeatureModelSerializer):
    """GeoJSON serializer for administrative areas."""

    class Meta:
        model = Area
        id_field = "uuid"
        geo_field = "geometry"
        exclude = ["id", "depth", "path", "numchild"]


class AreaEducationSerializer(BaseAreaEducationSerializer, GeoFeatureModelSerializer):
    """GeoJSON serializer for education aggregate statistics in administrative areas."""

    class Meta:
        model = Area
        id_field = "uuid"
        geo_field = "geometry"
        exclude = [
            "id",
            "depth",
            "path",
            "numchild",
            "population",
            "population_male",
            "population_female",
            "population_year",
            "area",
            "created_at",
            "updated_at",
        ]


class AreaEducationCSVSerializer(BaseAreaEducationSerializer):
    """Serializer for administrative areas and education statistics for CSV export."""

    class Meta:
        model = Area
        fields = [
            "uuid",
            "type_code",
            "country",
            "name",
            "code",
            "description",
            "institutions_count",
            "institutions_electrified",
            "institutions_fiber_connected",
            "institutions_electrified_no_fiber",
            "institutions_fiber_10km",
            "institutions_fiber_15km",
            "institutions_fiber_20km",
        ]
        read_only_fields = fields


class AreaEducationIFONDSerializer(BaseAreaEducationIFONDSerializer, GeoFeatureModelSerializer):
    """GeoJSON Serializer for summary education institutions statistics per administrative areas based on
    Fiber Optic Node/Network Distance."""

    class Meta:
        model = Area
        id_field = "uuid"
        geo_field = "geometry"
        exclude = [
            "id",
            "depth",
            "path",
            "numchild",
            "population",
            "population_male",
            "population_female",
            "population_year",
            "area",
            "created_at",
            "updated_at",
        ]


class AreaEducationIFONDCSVSerializer(BaseAreaEducationSerializer):
    """Serializer for summary education institutions statistics per administrative areas based on
    Fiber Optic Node/Network Distance for CSV export."""

    class Meta:
        model = Area
        fields = [
            "uuid",
            "type_code",
            "country",
            "name",
            "code",
            "description",
            "institutions_count",
            "institutions_electrified",
            "institutions_fiber_connected",
            "institutions_electrified_no_fiber",
        ]
        read_only_fields = fields


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
