from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"^layers/(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/(?P<path>.*)$",
        views.LayerTileXAccelRedirectView.as_view(),
        name="layer-tile-x-accel-redirect",
    ),
    re_path(
        r"^(?P<path>.*)$",
        views.MediaXAccelRedirectView.as_view(),
        name="x-accel-redirect",
    ),
]
