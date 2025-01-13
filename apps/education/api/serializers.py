from typing import List, Type

from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from administrative.models import Area

from ..models import Category, Institution, Ownership

__all__ = ["CategorySerializer", "OwnershipSerializer"]


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


class RelatedAreaSerializer(serializers.ModelSerializer):
    """A serializer for related administrative areas."""

    class Meta:
        model = Area
        fields = ["uuid", "name", "country"]


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


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Successful Response",
            value={
                "uuid": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Public",
                "code": "public",
                "description": "An institutions operated by local, state, or national governments.",
                "created_at": "2025-01-01T12:00:00Z",
                "updated_at": "2025-01-02T12:00:00Z",
                "extras": {"type": "academic"},
            },
            response_only=True,
        )
    ]
)
class OwnershipSerializer(serializers.ModelSerializer):

    class Meta:
        """Metadata for the :class:`OwnershipSerializer`.

        Attributes:
            model (Type[Ownership]):
                The model class that this serializer represents.

            fields (List[str]):
                The list of fields to be included in the serialized data.

            read_only_fields (List[str]):
                Fields that cannot be modified during updates.
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
        exclude = ["id"]
