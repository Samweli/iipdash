from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from administrative.api.serializers import RelatedAreaSerializer

from ..models import HealthFacility

__all__ = ["HealthFacilitySerializer"]


class HealthFacilitySerializer(GeoFeatureModelSerializer):

    administrative_area = RelatedAreaSerializer(read_only=True)

    class Meta:
        model = HealthFacility
        id_field = "uuid"
        geo_field = "geometry"
        exclude = ["id"]


class HealthFacilityCSVSerializer(serializers.ModelSerializer):
    """HealthFacility CSV serializer."""

    country = serializers.CharField(source="administrative_area.country", read_only=True)
    administrative_area_name = serializers.CharField(source="administrative_area.name", read_only=True)
    geometry = serializers.CharField()

    class Meta:
        model = HealthFacility
        fields = [
            "uuid",
            "name",
            "amenity",
            "osm_id",
            "osm_type",
            "administrative_area_name",
            "country",
            "created_at",
            "updated_at",
            "geometry",
        ]
        read_only_fields = fields
