from typing import List, Type

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from administrative.api.serializers import RelatedAreaSerializer

from ..models import Category, Institution, Ownership

__all__ = ["CategorySerializer", "OwnershipSerializer", "InstitutionSerializer", "InstitutionCSVSerializer"]


class RelatedCategorySerializer(serializers.ModelSerializer):
    """A serializer for related categories."""

    class Meta:
        model = Category
        fields = ["uuid", "name"]


class RelatedOwnershipSerializer(serializers.ModelSerializer):
    """A serializer for related ownership."""

    class Meta:
        model = Ownership
        fields = ["uuid", "name"]


class CategorySerializer(serializers.ModelSerializer):
    """Category of an educational institution."""

    class Meta:
        """Metadata for the :class:`CategorySerializer`.

        Attributes:
            model (Type[Category]):
                The model class that this serializer represents.

            fields (List[str]):
                A list of fields to be included in the serialized data.

            read_only_fields (List[str]):
                A list of fields that cannot be modified during updates.
        """

        model: Type[Category] = Category
        fields: List[str] = [
            "uuid",
            "name",
            "code",
            "description",
            "created_at",
            "updated_at",
            "extras",
        ]
        read_only_fields: List[str] = ["id", "uuid", "created_at", "updated_at"]


class OwnershipSerializer(serializers.ModelSerializer):
    """Ownership type of an educational institution."""

    class Meta:
        """Metadata for the :class:`OwnershipSerializer`.

        Attributes:
            model (Type[Ownership]):
                The model class that this serializer represents.

            fields (List[str]):
                A list of fields to be included in the serialized data.

            read_only_fields (List[str]):
                A list of fields that cannot be modified during updates.
        """

        model: Type[Ownership] = Ownership
        fields: List[str] = [
            "uuid",
            "name",
            "code",
            "description",
            "created_at",
            "updated_at",
            "extras",
        ]
        read_only_fields: List[str] = ["id", "uuid", "created_at", "updated_at"]


class InstitutionSerializer(GeoFeatureModelSerializer):

    category = RelatedCategorySerializer(read_only=True)
    ownership = RelatedOwnershipSerializer(read_only=True)
    administrative_area = RelatedAreaSerializer(read_only=True)

    class Meta:
        model = Institution
        id_field = "uuid"
        geo_field = "geometry"
        exclude = ["id", "related_areas"]


class InstitutionCSVSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    ownership = serializers.SlugRelatedField(slug_field="name", read_only=True)
    country = serializers.SerializerMethodField()
    administrative_area = serializers.SlugRelatedField(slug_field="name", read_only=True)
    geometry = serializers.CharField()

    class Meta:
        model = Institution
        fields = [
            "uuid",
            "category",
            "name",
            "ownership",
            "country",
            "administrative_area",
            "description",
            "code",
            "postal_code",
            "address",
            "phone",
            "fax",
            "email",
            "website",
            "has_electricity",
            "has_fiber_optic",
            "fon_distance",
            "osm_id",
            "osm_type",
            "created_at",
            "updated_at",
            "geometry",
        ]

        # There might be some performance gains in making fields read only
        # https://hakibenita.com/django-rest-framework-slow#read-only-modelserializer
        read_only_fields = fields

    def get_country(self, obj):
        if obj.administrative_area:
            return obj.administrative_area.country
