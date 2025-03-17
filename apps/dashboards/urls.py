from django.urls import path

from . import views

app_name = "dashboards"

urlpatterns = [
    # path("", views.HomeView.as_view(), name="home"),
    path("education/", views.EducationView.as_view(), name="education"),
    path("infrastructure", views.InfrastructureView.as_view(), name="infrastructure"),
]
