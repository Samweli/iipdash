from rest_framework_gis.serializers import GeoFeatureModelSerializer

from ..models import HealthFacility

__all__ = ["HealthFacilitySerializer"]


class HealthFacilitySerializer(GeoFeatureModelSerializer):

    class Meta:
        model = HealthFacility
        id_field = "uuid"
        geo_field = "geometry"
        exclude = ["id"]
