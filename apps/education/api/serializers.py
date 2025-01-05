from typing import List, Type

from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from ..models import Category, Ownership

__all__ = ["CategorySerializer", "OwnershipSerializer"]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Successful Response",
            value={
                "uuid": "550e8400-e29b-41d4-a716-446655440000",
                "name": "University",
                "code": "university",
                "description": "An institutions offering higher education.",
                "created_at": "2025-01-01T12:00:00Z",
                "updated_at": "2025-01-02T12:00:00Z",
                "extras": {"type": "academic"},
            },
            response_only=True,
        )
    ]
)
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        """Metadata for the :class:`CategorySerializer`.

        Attributes:
            model (Type[Category]):
                The model class that this serializer represents.

            fields (List[str]):
                The list of fields to be included in the serialized data.

            read_only_fields (List[str]):
                Fields that cannot be modified during updates.
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
