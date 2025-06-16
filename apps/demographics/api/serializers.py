from typing import List, Type

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from administrative.api.serializers import RelatedAreaSerializer

from ..models import PopulationDensityHD, RelativeWealthIndex

__all__ = ["PopulationDensityHDSerializer", "RelativeWealthIndexSerializer", "RelativeWealthIndexCSVSerializer"]


class PopulationDensityHDSerializer(GeoFeatureModelSerializer):
    administrative_area = RelatedAreaSerializer(read_only=True)

    class Meta:
        model = PopulationDensityHD
        id_field = "uuid"
        geo_field = "geometry"
        exclude = ["id", "geom"]


class RelativeWealthIndexSerializer(GeoFeatureModelSerializer):
    administrative_area = RelatedAreaSerializer(read_only=True)

    class Meta:
        model = RelativeWealthIndex
        id_field = "uuid"
        geo_field = "geometry"
        exclude = ["id"]


class RelativeWealthIndexCSVSerializer(serializers.ModelSerializer):
    """Relative Wealth Index CSV serializer."""

    country = serializers.CharField(source="administrative_area.country", read_only=True)
    administrative_area_name = serializers.CharField(source="administrative_area.name", read_only=True)
    geometry = serializers.CharField()

    class Meta:
        model: Type[RelativeWealthIndex] = RelativeWealthIndex
        fields: List[str] = [
            "uuid",
            "rwi",
            "error",
            "country",
            "administrative_area_name",
            "created_at",
            "updated_at",
            "geometry",
        ]
        read_only_fields: List[str] = fields
