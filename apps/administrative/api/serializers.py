from typing import List, Type

from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework_gis.fields import GeometrySerializerMethodField
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
    "AreaInternetSpeedSerializer",
    "AreaInternetSpeedCSVSerializer",
    "AreaHazardExposureSerializer",
    "AreaHazardExpsoureCSVSerializer",
    "RelatedAreaSerializer",
]


class BaseGeoFeatureModelSerializer(GeoFeatureModelSerializer):

    geometry = GeometrySerializerMethodField()
    country = serializers.CharField()

    def __init__(self, instance=None, data=empty, exclude_geometry=False, **kwargs):
        """If ``exclude_geometry`` is True, the serializer output when reading the instances won't include
        geometry coordinates.
        """
        self.exclude_geometry = exclude_geometry
        super().__init__(instance=instance, data=data, **kwargs)

    def get_geometry(self, obj):
        if self.exclude_geometry is True:
            return None
        return obj.geometry


class RelatedAreaSerializer(serializers.ModelSerializer):
    """A related administrative area."""

    country = serializers.CharField()

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


class AreaSerializer(BaseGeoFeatureModelSerializer):
    """GeoJSON serializer for administrative areas."""

    bbox = serializers.ListField(read_only=True)

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

    #: Number of education institutions with nearest fiber optic within 30km.
    institutions_fiber_30km = serializers.IntegerField(read_only=True)

    #: Average distance between education institutions and fiber optic nodes.
    institutions_fiber_distance_avg = serializers.IntegerField(read_only=True)

    #: Median distance between education institutions and fiber optic nodes.
    institutions_fiber_distance_median = serializers.IntegerField(read_only=True)


class AreaEducationSerializer(BaseAreaEducationSerializer, BaseGeoFeatureModelSerializer):
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
            "institutions_fiber_30km",
            "institutions_fiber_distance_avg",
            "institutions_fiber_distance_median",
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

    #: Average distance between education institutions and fiber optic nodes.
    institutions_fiber_distance_avg = serializers.IntegerField(read_only=True)

    #: Median distance between education institutions and fiber optic nodes.
    institutions_fiber_distance_median = serializers.IntegerField(read_only=True)


class AreaEducationIFONDSerializer(BaseAreaEducationIFONDSerializer, BaseGeoFeatureModelSerializer):
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
            "institutions_fiber_distance_avg",
            "institutions_fiber_distance_median",
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

    #: 2G Mobile coverage percentage.
    no_coverage_2g = serializers.FloatField(read_only=True)

    #: 3G Mobile coverage percentage.
    no_coverage_3g = serializers.FloatField(read_only=True)

    #: 4G Mobile coverage percentage.
    no_coverage_4g = serializers.FloatField(read_only=True)

    #: 5G Mobile coverage percentage.
    no_coverage_5g = serializers.FloatField(read_only=True)

    #: Population covered by 2G.
    population_covered_2g = serializers.IntegerField(read_only=True)

    #: Population covered by 3G.
    population_covered_3g = serializers.IntegerField(read_only=True)

    #: Population covered by 4G.
    population_covered_4g = serializers.IntegerField(read_only=True)

    #: Population covered by 5G.
    population_covered_5g = serializers.IntegerField(read_only=True)

    #: Population not covered by 2G.
    population_uncovered_2g = serializers.IntegerField(read_only=True)

    #: Population not covered by 3G.
    population_uncovered_3g = serializers.IntegerField(read_only=True)

    #: Population not covered by 4G.
    population_uncovered_4g = serializers.IntegerField(read_only=True)

    #: Population covered by 5G.
    population_uncovered_5g = serializers.IntegerField(read_only=True)


class AreaMobileCoverageSerializer(BaseAreaMobileCoverageSerializer, BaseGeoFeatureModelSerializer):
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
            "population_density_hd_avg",
            "population_covered_2g",
            "population_covered_3g",
            "population_covered_4g",
            "population_covered_5g",
            "population_uncovered_2g",
            "population_uncovered_3g",
            "population_uncovered_4g",
            "population_uncovered_5g",
            "coverage_2g",
            "coverage_3g",
            "coverage_4g",
            "coverage_5g",
            "no_coverage_2g",
            "no_coverage_3g",
            "no_coverage_4g",
            "no_coverage_5g",
        ]
        read_only_fields = fields


class AreaInternetSpeedSerializer(BaseGeoFeatureModelSerializer):
    fixed_speed = serializers.IntegerField(read_only=True)
    mobile_speed = serializers.IntegerField(read_only=True)

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
            "area",
            "population_male",
            "population_female",
        ]


class AreaInternetSpeedCSVSerializer(serializers.ModelSerializer):
    """Serializer for administrative areas internet speed CSV export."""

    class Meta:
        model = Area
        fields = [
            "uuid",
            "type_code",
            "country",
            "name",
            "code",
            "description",
            "mobile_speed",
            "fixed_speed",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class BaseAreaHazardExpsoureSerializer(serializers.ModelSerializer):

    population_exposed = serializers.IntegerField(read_only=True)
    population_exposed_percent = serializers.FloatField(read_only=True)
    population_exposed_ev = serializers.IntegerField(read_only=True)
    population_exposed_ev_percent = serializers.FloatField(read_only=True)


class AreaHazardExposureSerializer(BaseAreaHazardExpsoureSerializer, BaseGeoFeatureModelSerializer):
    """GeoJSON serializer for hazard exposure statistics in administrative areas."""

    class Meta:
        model = Area
        id_field = "uuid"
        geo_field = "geometry"
        fields = [
            "uuid",
            "name",
            "country",
            "population",
            "population_exposed",
            "population_exposed_percent",
            "population_exposed_ev",
            "population_exposed_ev_percent",
        ]


class AreaHazardExpsoureCSVSerializer(BaseAreaHazardExpsoureSerializer):
    """Serializer for administrative areas hazard exposure CSV export."""

    class Meta:
        model = Area
        fields = [
            "uuid",
            "type_code",
            "country",
            "name",
            "code",
            "description",
            "population_exposed",
            "population_exposed_ev",
            "urbanization_degree_codes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
