from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"^(?P<path>.*)$",
        views.MediaXAccelRedirectView.as_view(),
        name="x-accel-redirect",
    ),
]
