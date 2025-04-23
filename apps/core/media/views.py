from pathlib import Path

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.views import View

from catalog.models import Layer

from ..files import protected_filesystem_storage


class MediaXAccelRedirectView(View, LoginRequiredMixin):

    def get(self, request, path, *args, **kwargs):
        """Returns response including X-Accel-Redirect header for serving media file using another server
        typically Nginx."""

        path = Path(path)

        response = HttpResponse()
        response["X-Accel-Redirect"] = protected_filesystem_storage.internal_url(path)
        response["Content-Type"] = ""
        response["Content-Disposition"] = f'attachment; filename="{path.name}"'
        return response


class LayerTileXAccelRedirectView(View):

    def dispatch(self, request, *args, **kwargs):
        layer_uuid = self.kwargs["uuid"]
        if not Layer.objects.filter(uuid=layer_uuid, is_public=True).exists() and not request.user.is_authenticated:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, path, *args, **kwargs):
        """Returns response including X-Accel-Redirect header for serving tiles using another server
        typically Nginx."""
        layer_uuid = self.kwargs["uuid"]
        path = Path(f"layers/{layer_uuid}") / path

        response = HttpResponse()
        response["X-Accel-Redirect"] = protected_filesystem_storage.internal_url(path)
        response["Content-Type"] = ""
        response["Content-Disposition"] = f'attachment; filename="{path.name}"'
        return response
