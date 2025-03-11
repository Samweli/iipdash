from rest_framework import serializers

from ..models import Category, Layer


class RelatedCategorySerializer(serializers.ModelSerializer):
    """Category Relation Serializer"""

    class Meta:
        model = Category
        fields = [
            "uuid",
            "name",
            "code",
        ]


class CategorySerializer(serializers.ModelSerializer):
    """Catalog Category Serializer"""

    class Meta:
        model = Category
        fields = [
            "uuid",
            "name",
            "code",
            "description",
            "created_at",
            "updated_at",
        ]


class LayerSerializer(serializers.ModelSerializer):
    """Layer Serializer"""

    categories = RelatedCategorySerializer(read_only=True)

    class Meta:
        model = Layer
        exclude = ["id"]
