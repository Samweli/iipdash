import uuid

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Envelope
from django.contrib.gis.geos import Point
from django.db.models.functions import Cast, Now
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from administrative.models import Area
from core.aggregation import StBuffer


class PopulationDensityHD(models.Model):
    """High resolution population density."""

    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_("A universally unique identifier (UUID) for the area."),
    )

    administrative_area = models.ForeignKey(
        "administrative.Area",
        blank=True,
        null=True,
        related_name="population_densities_hd",
        related_query_name="population_density_hd",
        on_delete=models.SET_NULL,
        verbose_name=_("administrative area"),
        help_text=_("The administrative area to which the population density belongs."),
    )

    geometry = models.PointField(
        _("location"),
        geography=True,
        srid=4326,
        help_text=_("The geospatial location."),
    )

    #: A version of geometry optimized for performant rendering.
    geom = models.PointField(
        _("geom"),
        geography=False,
        blank=True,
        null=True,
        srid=3857,
        editable=False,
        help_text=_("A version of geometry optimized for performant rendering."),
    )

    population_density = models.FloatField(
        _("population density"),
        help_text=_("population in 1-arc-second-by-1-arc-second grid (30.87-meter-by-30.87 at the equator)"),
        db_index=True,
    )

    year = models.PositiveIntegerField(_("year"), blank=True, null=True)

    #: The database level timestamp of when the area was created.
    created_at = models.DateTimeField(
        "created at",
        auto_now_add=True,
        db_default=Now(),
        help_text=_("The database level timestamp of when the record was created."),
    )

    #: The database level timestamp of when the area was latest modified.
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        null=True,
        blank=True,
        help_text=_("Timestamp of when the record was last modified."),
    )

    class Meta:
        verbose_name = _("Population Density (HD)")
        verbose_name_plural = _("Population Densities (HD)")
        indexes = [
            models.Index(fields=["administrative_area", "population_density"], name="admin_area_pop_density_idx"),
        ]

    def save(self, *args, **kwargs):
        self.geom = self.geometry2geom()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.geometry.wkt} {self.population_density}"

    def geometry2geom(self):
        """Transform geometry to simplified EPSG:3857"""

        if self.geometry:
            geom = self.geometry.transform(3857, clone=True)
            return Point(round(geom.x, 1), round(geom.y, 1), srid=geom.srid)


class RelativeWealthIndex(models.Model):
    """Relative wealth Index."""

    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_("A universally unique identifier (UUID)."),
    )

    administrative_area = models.ForeignKey(
        "administrative.Area",
        blank=True,
        null=True,
        related_name="relative_wealth_indexes",
        related_query_name="relative_wealth_index",
        on_delete=models.SET_NULL,
        verbose_name=_("administrative area"),
        help_text=_("The administrative area to which the relative wealth index belongs."),
    )

    geometry = models.PointField(
        _("location"),
        geography=True,
        srid=4326,
        help_text=_("The geo-spatial location."),
    )

    bounds = models.PolygonField(
        _("bounds"), blank=True, null=True, geography=True, help_text=_("Boundaries of the area covered")
    )

    rwi = models.FloatField(_("rwi"))
    error = models.FloatField(_("error"), blank=True, null=True)

    #: The database level timestamp of when the area was created.
    created_at = models.DateTimeField(
        "created at",
        auto_now_add=True,
        db_default=Now(),
        help_text=_("The database level timestamp of when the record was created."),
    )

    #: The database level timestamp of when the area was latest modified.
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        null=True,
        blank=True,
        help_text=_("Timestamp of when the record was last modified."),
    )

    class Meta:
        verbose_name = _("Relative Wealth Index")
        verbose_name_plural = _("Relative Wealth Indexes")

    def __str__(self):
        return f"{str(self.geometry)}: {self.rwi}"

    def save(self, *args, **kwargs):
        self.set_administrative_area(overwrite=False)
        super().save(*args, **kwargs)
        self.update_bounds(overwrite=False)

    def set_administrative_area(self, overwrite=True):
        """Try to detect related administrative area based on the location if not yet provided."""
        if (self.administrative_area is not None and overwrite is not True) or self.geometry is None:
            return

        area = Area.objects.filter(geometry__covers=self.geometry).order_by("-depth").first()
        if area:
            self.administrative_area = area

    def update_bounds(self, overwrite=True):
        if (self.bounds is not None and overwrite is not True) or self.geometry is None:
            return

        buffer_size = settings.RELATIVE_WEALTH_INDEX_RESOLUTION / 2

        RelativeWealthIndex.objects.filter(pk=self.pk).update(
            updated_at=now(),
            bounds=Envelope(
                Cast(
                    StBuffer("geometry", buffer_size),
                    models.PolygonField(),
                ),
            ),
        )

        self.refresh_from_db()
