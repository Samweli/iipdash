from pathlib import Path

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View

from .files import protected_filesystem_storage


class MediaXAccelRedirectView(View, LoginRequiredMixin):

    def get(self, request, path, *args, **kwargs):
        """Returns response including X-Accel-Redirect header for serving media file using another server
        typically Nginx."""

        path = Path(path)

        response = HttpResponse()
        response["X-Accel-Redirect"] = protected_filesystem_storage.redirect_url(path)
        response["Content-Type"] = ""
        response["Content-Disposition"] = f'attachment; filename="{path.name}"'
        return response
