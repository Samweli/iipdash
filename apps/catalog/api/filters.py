from django.utils.translation import gettext_lazy as _

from django_filters import rest_framework as filters

from ..models import Layer

__all__ = ["LayerFilter"]


class LayerFilter(filters.FilterSet):

    category = filters.UUIDFilter(
        field_name="categories__uuid",
        help_text=_("Filter by category UUID."),
        label=_("category UUID"),
    )

    category_name = filters.CharFilter(
        field_name="categories__name",
        help_text=_("Filter by category name."),
        label=_("category name"),
    )

    category_code = filters.CharFilter(
        field_name="categories__code",
        help_text=_("Filter by category code."),
        label=_("category code"),
    )

    #: Filter by multiple administrative area UUIDs
    categories = filters.BaseInFilter(
        field_name="categories__uuid",
        help_text=_("Filter by multiple categories UUIDs."),
    )

    tags = filters.BaseInFilter(
        field_name="tags",
        lookup_expr="contains",
        help_text=_("Filter by multiple categories UUIDs."),
    )

    name = filters.CharFilter(
        lookup_expr="iexact",
        help_text=_("Filter by category code."),
    )

    source = filters.CharFilter(
        lookup_expr="iexact",
        help_text=_("Filter by category code."),
    )

    class Meta:

        model = Layer
        fields = ["name", "category", "category_name", "category_code", "categories", "source", "source_url"]
