from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class EducationDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboards/education.html"
