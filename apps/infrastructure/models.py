import uuid

from django.contrib.gis import geos
from django.contrib.gis.db import models
from django.core.validators import MinValueValidator
from django.db.models.functions import Now
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField


class OpticalFibre(models.Model):
    """An optical fibre network data model."""

    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    country = CountryField(_("country"), blank=True, db_index=True)

    name = models.CharField(_("name"), max_length=255, blank=True)
    description = models.TextField(_("description"), blank=True)

    geometry = models.MultiLineStringField(
        _("geometry"),
        geography=True,
        blank=True,
        null=True,
        srid=4326,
    )

    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        db_default=Now(),
        db_index=True,
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        null=True,
        blank=True,
    )
    extras = models.JSONField(_("extras"), blank=True, default=dict)

    class Meta:
        verbose_name = _("Optical Fibre Network")
        verbose_name_plural = _("Optical Fibre Networks")

    def save(self, *args, **kwargs):
        if self.geometry and isinstance(self.geometry, geos.LineString):
            self.geometry = geos.MultiLineString(self.geometry)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or format_lazy(
            "Optical Fibre: {country}: {uuid}",
            country=self.country,
            uuid=self.uuid,
        )


class CellTower(models.Model):
    """A cell tower data model."""

    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    network_type = models.CharField(
        _("network type"),
        max_length=255,
        blank=True,
        help_text=_("Examples; GSM, UMTS, LTE or CDMA."),
    )

    mcc = models.SmallIntegerField(
        _("mobile country code"),
        blank=True,
        null=True,
        help_text=_("Example 265 for Malawi"),
    )

    geometry = models.PointField(
        _("location"),
        geography=True,
        blank=True,
        null=True,
        srid=4326,
    )

    #: Defines if coordinates of the cell tower are exact or approximate.
    location_is_approximate = models.BooleanField(
        _("location is approximate"),
        blank=True,
        null=True,
    )

    range = models.FloatField(
        _("range (meters)"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=_("Estimate of cell range"),
    )

    administrative_area = models.ForeignKey(
        "administrative.Area",
        blank=True,
        null=True,
        related_name="infrastructure_cell_towers",
        related_query_name="infrastructure_cell_tower",
        on_delete=models.SET_NULL,
        verbose_name=_("administrative area"),
    )

    src_created = models.DateTimeField(
        _("source record created at"),
        null=True,
        blank=True,
    )
    src_updated_at = models.DateTimeField(
        _("source record updated at"),
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        db_default=Now(),
        db_index=True,
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        null=True,
        blank=True,
    )
    extras = models.JSONField(_("extras"), blank=True, default=dict)

    class Meta:
        verbose_name = _("Cell Tower")
        verbose_name_plural = _("Cell Towers")

    @property
    def display_name(self):
        return format_lazy(
            "{network_type} cell tower: {uuid}",
            network_type=self.network_type,
            uuid=self.uuid,
        )

    def __str__(self):
        return self.display_name
