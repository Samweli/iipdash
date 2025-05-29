import csv

from django.http import Http404, StreamingHttpResponse
from django.utils.timezone import now

from ..utils import PseudoBuffer

__all__ = ["CSVDownloadMixin"]


class CSVDownloadMixin:
    """CSV download Mixin. Provides a `export_csv()` method returning streaming CSV response.

    Expected to used with Generic Views and Viewsets from Django Rest Framework.
    """

    #: DRF serializer class used for serializing objects data.
    csv_serializer_class = None

    def get_csv_serializer_class(self):
        """Return the class to use for the CSV serializer.
        Defaults to using `self.get_serializer_class()`.

        You may want to override this if you need to provide different
        serializations for CSV exports or depending on the incoming request.
        """
        if self.csv_serializer_class:
            return self.csv_serializer_class
        else:
            return self.get_serializer_class()

    def get_csv_queryset(self):
        """Return a queryset used for CSV generation.
        Defaults to using queryset from `self.get_queryset()`.
        """
        return self.get_queryset()

    def stream_csv(self):
        """Yields buffered CSV rows"""
        serializer_class = self.get_csv_serializer_class()
        queryset = self.filter_queryset(self.get_csv_queryset())

        field_names = serializer_class().get_fields().keys()

        pseudo_buffer = PseudoBuffer()
        writer = csv.DictWriter(pseudo_buffer, fieldnames=field_names)

        yield writer.writeheader()

        for row in queryset.iterator():
            yield writer.writerow(self.csv_serializer_class(row).data)

    def get_csv_file_name(self):
        """Return name of the CSV file produced."""
        model_name = self.get_queryset().model._meta.object_name.lower()
        return f"{model_name}-{now().date()}.csv"

    def export_csv(self, request, *args, **kwargs):
        """Export data as CSV file for authenticated users.

        Returns:
            django.http.StreamingHttpResponse
        """

        if not request.user.is_authenticated:
            raise Http404

        file_name = self.get_csv_file_name()

        return StreamingHttpResponse(
            self.stream_csv(),
            content_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
        )
