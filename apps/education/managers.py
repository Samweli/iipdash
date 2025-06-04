from itertools import islice

from django.apps import apps
from django.contrib.gis.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.gis.db.models.functions import Distance
from django.db.models import ExpressionWrapper, OuterRef, Subquery
from django.utils import timezone


class InstitutionQuerySet(models.QuerySet):

    def calculate_fon_distance(self):
        """Annotates a queryset with distance to the nearest fiber optic node in a country
        (``calculated_fon_distance`` attribute) calculated in realtime based on fiber optic nodes
        in the database.

        Returns:
            django.models.db.QuerySet.
        """

        fiber_node_model = apps.get_registered_model("infrastructure", "FiberOpticNode")

        nearest_nodes = (
            fiber_node_model.objects.filter(administrative_area__country=OuterRef("administrative_area__country"))
            .annotate(
                distance=Distance(
                    "geometry",
                    ExpressionWrapper(
                        OuterRef("geometry"),
                        output_field=PointField(),
                    ),
                )
            )
            .order_by("distance")
        )

        return self.annotate(calculated_fon_distance=Subquery(nearest_nodes.values("distance")[:1]))

    def refresh_fon_distances(self, batch_size=1000):
        """Updates the ``fon_distance`` attribute of the objects matching the queryset based on
         distance to the nearest fiber optic node in a country calculated in real time.

        Args:
            batch_size (int):
                Maximum number of records that can be processed in a single query.

        Returns:
            int: number of updated objects.
        """

        objs = self.calculate_fon_distance().iterator(chunk_size=batch_size)
        updated = 0

        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break

            now = timezone.now()
            for obj in batch:
                if obj.calculated_fon_distance is not None:
                    obj.fon_distance = obj.calculated_fon_distance.m
                else:
                    obj.fon_distance = None
                obj.updated_at = now

            updated += self.bulk_update(batch, ["fon_distance", "updated_at"], batch_size=batch_size)

        return updated


class InstitutionManager(models.Manager):
    """Education Institutions model manager."""

    def get_queryset(self):
        return InstitutionQuerySet(self.model, using=self._db)

    def calculate_fon_distance(self):
        return self.get_queryset().calculate_fon_distance()

    def refresh_fon_distances(self, batch_size=1000):
        return self.get_queryset().refresh_fon_distances(batch_size=batch_size)
