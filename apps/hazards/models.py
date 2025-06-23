import uuid
from pathlib import Path
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.gdal import GDALRaster
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _

from .files import hazard_exposure_tiff_path


class Hazard(models.Model):
    """A hazard type."""

    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    name = models.CharField(
        _("name"),
        max_length=255,
        db_index=True,
    )

    code = models.SlugField(
        _("code"),
        blank=True,
        null=True,
        max_length=50,
        unique=True,
    )

    description = models.TextField(_("description"), blank=True, help_text=_("A long-form description."))

    created_at = models.DateTimeField(
        "created at",
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

    extras = models.JSONField(
        _("extras"),
        blank=True,
        default=dict,
    )

    class Meta:
        verbose_name = _("Hazard")
        verbose_name_plural = _("Hazards")

    def __str__(self):
        return self.name


class UrbanizationDegree(models.Model):
    """Degree of Urbanization."""

    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    name = models.CharField(
        _("name"),
        max_length=255,
        db_index=True,
    )

    code = models.SlugField(
        _("code"),
        blank=True,
        null=True,
        max_length=50,
        unique=True,
    )

    description = models.TextField(_("description"), blank=True, help_text=_("A long-form description."))

    created_at = models.DateTimeField(
        "created at",
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

    extras = models.JSONField(
        _("extras"),
        blank=True,
        default=dict,
    )

    class Meta:
        verbose_name = _("Degree of Urbanization")
        verbose_name_plural = _("Degrees of Urbanization")

    def __str__(self):
        return self.name


class ExposureCoverage(models.Model):
    """Hazard exposure coverage per administrative area."""

    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    administrative_area = models.ForeignKey(
        "administrative.Area",
        blank=True,
        null=True,
        related_name="hazards_exposure_coverages",
        related_query_name="hazards_exposure_coverage",
        on_delete=models.SET_NULL,
        verbose_name=_("administrative area"),
    )

    tiff = models.FileField(
        _("hazard exposure GeoTIFF"),
        upload_to=hazard_exposure_tiff_path,
        max_length=510,
        blank=True,
        help_text=_("The file is expected to contain one band."),
    )

    #: PostGIS raster
    raster = models.RasterField(
        _("hazard exposure"),
        srid=4326,
        blank=True,
        null=True,
        editable=False,
        help_text=_("hazard exposure raster data stored in the database."),
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

    extras = models.JSONField(
        _("extras"),
        blank=True,
        default=dict,
    )

    class Meta:
        verbose_name = _("Hazard Exposure Coverage")
        verbose_name_plural = _("Hazard Exposure Coverages")

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        return _("%(area)s hazards exposure coverage") % {
            "area": str(self.administrative_area),
        }

    @property
    def tiles_dir(self):
        return Path(f"hazards-coverage/{self.uuid}/")

    @property
    def tiles_root(self):
        return Path(settings.TILES_ROOT) / self.tiles_dir

    @property
    def tms_url(self):
        if not self.tiff:
            return None

        return urljoin(settings.TILES_URL, f"{self.tiles_dir}/{{z}}/{{x}}/{{y}}.png")

    def set_raster(self):
        """Set raster attribute data based on assigned GeoTIFF file."""
        if not self.tiff:
            return

        raster = GDALRaster(self.tiff.read())
        raster_srid = self._meta.model.raster.field.srid

        if raster.srid != raster_srid:
            raster = raster.transform(raster_srid)

        self.raster = raster


class HazardExposure(models.Model):
    """Hazard exposure summary per administrative area."""

    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    coverage = models.ForeignKey(
        ExposureCoverage,
        blank=True,
        null=True,
        related_name="exposures",
        related_query_name="exposure",
        on_delete=models.SET_NULL,
        verbose_name=_("coverage"),
    )

    urbanization_degree = models.ForeignKey(
        UrbanizationDegree,
        on_delete=models.SET_NULL,
        related_name="exposures",
        related_query_name="exposure",
        blank=True,
        null=True,
        verbose_name=_("degree of urbanization"),
    )

    hazards = models.ManyToManyField(
        Hazard,
        related_name="exposures",
        related_query_name="exposure",
        blank=True,
        verbose_name=_("hazards"),
    )

    population_exposed = models.PositiveIntegerField(_("population exposed"), blank=True, null=True)
    population_exposed_percent = models.FloatField(_("population exposed (percentage)"), blank=True, null=True)

    population_exposed_ev = models.PositiveIntegerField(
        _("economically vulnerable population exposed"), blank=True, null=True
    )
    population_exposed_ev_percent = models.FloatField(
        _("economically vulnerable population exposed (percentage)"), blank=True, null=True
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

    extras = models.JSONField(
        _("extras"),
        blank=True,
        default=dict,
    )

    class Meta:
        verbose_name = _("Hazards Exposure")
        verbose_name_plural = _("Hazards Exposures")

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        return _("%(area)s %(hazards)s exposure") % {
            "area": str(self.coverage.administrative_area),
            "hazards": ", ".join([str(hazard) for hazard in self.hazards.all()]),
        }
