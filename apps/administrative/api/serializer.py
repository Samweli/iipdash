from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from ..models import Area

__all__ = ["AreaSerializer", "AreaEducationSerializer"]


class AreaSerializer(GeoFeatureModelSerializer):
    """GeoJSON serializer for administrative areas."""

    class Meta:
        model = Area
        id_field = "uuid"
        geo_field = "geometry"
        exclude = ["id", "depth", "path", "numchild"]


class AreaEducationSerializer(GeoFeatureModelSerializer):
    """GeoJSON serializer for administrative areas."""

    institutions_count = serializers.SerializerMethodField()
    institutions_electrified = serializers.SerializerMethodField()
    institutions_fiber_connected = serializers.SerializerMethodField()
    institutions_electrified_no_fiber = serializers.SerializerMethodField()
    institutions_fiber_10km = serializers.SerializerMethodField()
    institutions_fiber_15km = serializers.SerializerMethodField()
    institutions_fiber_20km = serializers.SerializerMethodField()

    class Meta:
        model = Area
        id_field = "uuid"
        geo_field = "geometry"
        exclude = ["id", "depth", "path", "numchild"]

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
