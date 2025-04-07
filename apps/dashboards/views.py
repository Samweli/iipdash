from typing import Any, Dict, List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from catalog.models import Category, Layer


class EducationView(LoginRequiredMixin, TemplateView):
    template_name = "dashboards/education.html"


class InfrastructureView(LoginRequiredMixin, TemplateView):
    template_name = "dashboards/infrastructure.html"


class HomeView(LoginRequiredMixin, TemplateView):
    """View for rendering the home page."""

    template_name = "about/home.html"

    def get_catalog_categories(self) -> List[Category]:
        """Retrieves all catalog categories.

        Returns:
            List[Category]: A list of Category objects.
        """
        categories = Category.objects.all().order_by("name")
        return categories

    def get_catalog_layers(self) -> List[Layer]:
        """Retrieves all catalog layers.

        Returns:
            List[Layer]: A list of Layer objects.
        """
        queryset = Layer.objects.prefetch_related("categories")
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_public=True)
        layers = queryset.all().order_by("name")
        return layers

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Gets the context data for the home page.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            Dict[str, Any]: A dictionary containing the context data.
        """
        context = super().get_context_data(**kwargs)
        context["catalog_categories"] = self.get_catalog_categories()
        context["catalog_layers"] = self.get_catalog_layers()
        return context
