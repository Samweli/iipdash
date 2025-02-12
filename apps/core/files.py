from django.core.files.storage import FileSystemStorage
from django.urls import reverse


class ProtectedFileSystemStorage(FileSystemStorage):

    def url(self, name):
        """Returns protected URL to the file. This allows custom handling of the
        process of granting access to the file."""

        return reverse("x-accel-redirect", kwargs={"path": name})

    def redirect_url(self, name):
        return super().url(name)


protected_filesystem_storage = ProtectedFileSystemStorage()
