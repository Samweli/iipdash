from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.utils.encoding import filepath_to_uri


class ProtectedFileSystemStorage(FileSystemStorage):

    def url(self, name):
        """Returns protected URL to the file. This allows custom handling of the
        process of granting access to the file."""

        return reverse("x-accel-redirect", kwargs={"path": name})

    def internal_url(self, name):
        url = filepath_to_uri(name)

        if url is not None:
            url = url.lstrip("/")
        return urljoin(settings.MEDIA_INTERNAL_URL, url)


protected_filesystem_storage = ProtectedFileSystemStorage()
