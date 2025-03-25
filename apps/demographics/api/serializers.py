from rest_framework_gis.serializers import GeoFeatureModelSerializer

from administrative.api.serializers import RelatedAreaSerializer

from ..models import PopulationDensityHD, RelativeWealthIndex

__all__ = ["PopulationDensityHDSerializer", "RelativeWealthIndexSerializer"]


class PopulationDensityHDSerializer(GeoFeatureModelSerializer):
    administrative_area = RelatedAreaSerializer(read_only=True)

    class Meta:
        model = PopulationDensityHD
        id_field = "uuid"
        geo_field = "geometry"
        exclude = ["id", "geom"]


class RelativeWealthIndexSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = RelativeWealthIndex
        id_field = "uuid"
        geo_field = "geometry"
        exclude = ["id"]
