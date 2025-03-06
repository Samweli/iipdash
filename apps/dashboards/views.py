from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class EducationView(LoginRequiredMixin, TemplateView):
    template_name = "dashboards/education.html"


class InfrastructureView(LoginRequiredMixin, TemplateView):
    template_name = "dashboards/infrastructure.html"
