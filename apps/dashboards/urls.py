from django.urls import path

from . import views

app_name = "dashboards"

urlpatterns = [
    path("education/", views.EducationView.as_view(), name="education"),
    path("infrastructure", views.InfrastructureView.as_view(), name="infrastructure"),
    path("hazard", views.HazardView.as_view(), name="hazard"),
]
