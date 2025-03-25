import uuid

from django.contrib.gis.db import models
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _


class HealthFacility(models.Model):
    """A Health Facility"""

    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    name = models.CharField(_("name"), max_length=255, blank=True)

    amenity = models.CharField(_("amenity"), max_length=50, blank=True)

    #: The geospatial location of the facility.
    geometry = models.PointField(
        _("location"),
        geography=True,
        blank=True,
        null=True,
        srid=4326,
    )

    #: OpenStreetMap ID of the institution.
    osm_id = models.BigIntegerField(_("OSM id"), blank=True, null=True)

    #: OpenStreetMap type of the institution.
    osm_type = models.CharField(_("OSM type"), max_length=255, blank=True)

    #: The database level timestamp of when the record was created.
    created_at = models.DateTimeField(
        "created at",
        auto_now_add=True,
        db_default=Now(),
        db_index=True,
        help_text=_("The database level timestamp of when the record was created."),
    )

    #: The database level timestamp of when the record was last modified.
    updated_at = models.DateTimeField(
        _("updated_at"),
        auto_now=True,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Health Facility")
        verbose_name_plural = _("Health Facilities")

    def __str__(self):
        return self.name
