from typing import List, Type

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from ..models import Area

__all__ = [
    "AreaSerializer",
    "AreaCSVSerializer",
    "BaseAreaEducationSerializer",
    "AreaEducationSerializer",
    "AreaEducationCSVSerializer",
    "BaseAreaEducationIFONDSerializer",
    "AreaEducationIFONDSerializer",
    "AreaEducationIFONDCSVSerializer",
    "BaseAreaMobileCoverageSerializer",
    "AreaMobileCoverageSerializer",
    "AreaMobileCoverageCSVSerializer",
    "RelatedAreaSerializer",
]


class AreaSerializer(GeoFeatureModelSerializer):
    """GeoJSON serializer for administrative areas."""

    class Meta:
        model = Area
        id_field = "uuid"
        geo_field = "geometry"
        exclude = ["id", "depth", "path", "numchild", "geom"]


class AreaCSVSerializer(serializers.ModelSerializer):
    """Serializer for administrative areas for CSV export."""

    class Meta:
        model = Area
        fields = [
            "uuid",
            "type_code",
            "country",
            "name",
            "code",
            "description",
            "area",
            "population",
            "population_year",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class BaseAreaEducationSerializer(serializers.ModelSerializer):
    """Base class for Education summary per administrative areas"""

    #: Number of electrified education institutions.
    institutions_count = serializers.IntegerField(read_only=True)

    #: Number of electrified education institutions.
    institutions_electrified = serializers.IntegerField(read_only=True)

    #: Number of education institutions connected to fiber optic.
    institutions_fiber_connected = serializers.IntegerField(read_only=True)

    #: Number of electrified education institutions not connected to fiber optic
    institutions_electrified_no_fiber = serializers.IntegerField(read_only=True)

    #: Number of education institutions with nearest fiber optic within 10km.
    institutions_fiber_10km = serializers.IntegerField(read_only=True)

    #: Number of education institutions with nearest fiber optic within 15km.
    institutions_fiber_15km = serializers.IntegerField(read_only=True)

    #: Number of education institutions with nearest fiber optic within 20km.
    institutions_fiber_20km = serializers.IntegerField(read_only=True)


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
            "geom",
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


class BaseAreaEducationIFONDSerializer(serializers.ModelSerializer):
    """Base serializer clas for summary education institutions statistics per administrative areas based on
    Fiber Optic Node/Network Distance."""

    #: Number of electrified education institutions.
    institutions_count = serializers.IntegerField(read_only=True)

    #: Number of electrified education institutions.
    institutions_electrified = serializers.IntegerField(read_only=True)

    #: Number of education institutions connected to fiber optic.
    institutions_fiber_connected = serializers.IntegerField(read_only=True)

    #: Number of electrified education institutions not connected to fiber optic
    institutions_electrified_no_fiber = serializers.IntegerField(read_only=True)


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
            "geom",
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


class BaseAreaMobileCoverageSerializer(serializers.ModelSerializer):

    #: 2G Mobile coverage percentage.
    coverage_2g = serializers.FloatField(read_only=True)

    #: 3G Mobile coverage percentage.
    coverage_3g = serializers.FloatField(read_only=True)

    #: 4G Mobile coverage percentage.
    coverage_4g = serializers.FloatField(read_only=True)

    #: 5G Mobile coverage percentage.
    coverage_5g = serializers.FloatField(read_only=True)

    #: Population covered by 2G.
    population_covered_2g = serializers.IntegerField(read_only=True)

    #: Population covered by 3G.
    population_covered_3g = serializers.IntegerField(read_only=True)

    #: Population covered by 4G.
    population_covered_4g = serializers.IntegerField(read_only=True)

    #: Population covered by 5G.
    population_covered_5g = serializers.IntegerField(read_only=True)


class AreaMobileCoverageSerializer(BaseAreaMobileCoverageSerializer, GeoFeatureModelSerializer):
    """GeoJSON serializer for mobile coverage statistics in administrative areas."""

    class Meta:
        model = Area
        id_field = "uuid"
        geo_field = "geometry"
        exclude = [
            "id",
            "depth",
            "path",
            "numchild",
            "geom",
            "population_male",
            "population_female",
            "created_at",
            "updated_at",
        ]


class AreaMobileCoverageCSVSerializer(BaseAreaMobileCoverageSerializer):
    """CSV serializer for mobile coverage statistics in administrative areas."""

    class Meta:
        model = Area
        fields = [
            "uuid",
            "type_code",
            "country",
            "name",
            "code",
            "description",
            "population",
            "population_year",
            "population_covered_2g",
            "population_covered_3g",
            "population_covered_4g",
            "population_covered_5g",
            "coverage_2g",
            "coverage_3g",
            "coverage_4g",
            "coverage_5g",
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
