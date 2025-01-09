from rest_framework_gis.serializers import GeoFeatureModelSerializer

from ..models import Area

__all__ = ["AreaSerializer"]


class AreaSerializer(GeoFeatureModelSerializer):
    """GeoJSON serializer for administrative areas."""

    class Meta:
        model = Area
        id_field = "uuid"
        geo_field = "geometry"
        exclude = ["id", "depth", "path", "numchild"]
