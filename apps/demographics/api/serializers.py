from rest_framework_gis.serializers import GeoFeatureModelSerializer

from administrative.api.serializers import RelatedAreaSerializer

from ..models import PopulationDensityHD

__all__ = ["PopulationDensityHDSerializer"]


class PopulationDensityHDSerializer(GeoFeatureModelSerializer):
    administrative_area = RelatedAreaSerializer(read_only=True)

    class Meta:
        model = PopulationDensityHD
        id_field = "uuid"
        geo_field = "geometry"
        exclude = ["id", "geom"]
