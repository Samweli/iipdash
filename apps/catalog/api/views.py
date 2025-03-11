from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import Category, Layer
from .filters import LayerFilter
from .serializers import CategorySerializer, LayerSerializer


@extend_schema_view(
    list=extend_schema(
        description=_("Retrieve a list of catalog categories"),
        summary=_("Catalog Categories"),
    ),
    retrieve=extend_schema(
        description=_("Retrieve details of a specific catalog category."),
        summary=_("Catalog Category"),
    ),
)
class CategoryViewSet(ReadOnlyModelViewSet):
    """Catalog Category endpoint"""

    serializer_class = CategorySerializer
    lookup_field = "uuid"

    #: A list of required OAuth2 scopes for accessing the `Category` API endpoints.
    required_scopes = ["default"]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    filterset_fields = ["code"]
    search_fields = ["name", "code"]

    #: A list of fields that are used for ordering the queryset of
    #: `Category` objects (e.g., `?ordering=<field>`).
    ordering_fields = ["name", "created_at", "updated_at"]

    #: A default queryset for retrieving `Category` objects.
    queryset = Category.objects.all().order_by("name")


@extend_schema_view(
    list=extend_schema(
        description=_("Retrieve a list of layers"),
        summary=_("Layers"),
    ),
    retrieve=extend_schema(
        description=_("Retrieve details of a specific layer"),
        summary=_("Layer"),
    ),
)
class LayerViewSet(ReadOnlyModelViewSet):
    """Layers Catalog endpoint"""

    serializer_class = LayerSerializer
    lookup_field = "uuid"

    #: A list of required OAuth2 scopes for accessing the `Category` API endpoints.
    required_scopes = ["default"]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    filterset_class = LayerFilter
    search_fields = ["name", "code"]

    #: A list of fields that are used for ordering the queryset of
    #: `Category` objects (e.g., `?ordering=<field>`).
    ordering_fields = ["name", "created_at", "updated_at"]

    def get_queryset(self):
        """Return a queryset of Layers.

        If the user is not authenticated only public layers are returned.
        """
        queryset = Layer.objects.prefetch_related("categories")
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_public=True)

        return queryset.order_by("-created_at")
