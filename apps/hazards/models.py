import shutil
import uuid
from pathlib import Path
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.gdal import GDALRaster
from django.contrib.postgres.fields import ArrayField
from django.db.models.functions import Now
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

import gdal2tiles
import numpy as np
import rasterio
from rasterio.enums import ColorInterp

from .colormaps import exposure_coverage_colormap
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

    def clear_tiles(self):
        try:
            shutil.rmtree(self.tiles_root)
        except FileNotFoundError:
            pass

    def generate_tiles(self, **kwargs):
        """Generate tiles for using web maps from TIFF file."""

        if not self.tiff:
            return

        rgb_tiff = self.band2rgba()

        kwargs = {
            "webviewer": "none",
            "nb_processes": settings.GDAL2TILES_PROCESSES,
            "profile": "mercator",
            "tile_size": 256,
            "tmscompatible": True,
            "zoom": (1, 15),
            **kwargs,
        }

        self.clear_tiles()
        gdal2tiles.generate_tiles(str(rgb_tiff), str(self.tiles_root), **kwargs)

    def band2rgba(self):
        """Converts a single band coverage GeoTIFF to RGBA format.

        Returns:
            Path: Path to the created RGBA GeoTIFF file.
        """
        dataset = rasterio.open(self.tiff.open())
        data_band = dataset.read(1)

        og_file_name = Path(self.tiff.name).name
        rgb_rel_path = f"hazards/hazard-exposure/{self.uuid}/tiff-rgba/{og_file_name}"
        rgb_path = Path(settings.MEDIA_ROOT) / rgb_rel_path
        Path.mkdir(rgb_path.parent, parents=True, exist_ok=True)

        # output profile
        output_profile = {
            "driver": "GTiff",
            "width": dataset.shape[1],
            "height": dataset.shape[0],
            "count": 4,
            "crs": dataset.crs,
            "transform": dataset.transform,
            "dtype": "uint8",
            "photometric": "RGBA",
        }

        try:
            colormap = dataset.colormap(1)
        except ValueError:
            colormap = None

        if colormap:
            rgba_band = np.full((4, data_band.shape[0], data_band.shape[1]), dataset.nodata, dtype=np.uint8)

            colormap.update(exposure_coverage_colormap)

            for index, color in colormap.items():
                rgba_band[0][data_band == index] = color[0]  # Red
                rgba_band[1][data_band == index] = color[1]  # Green
                rgba_band[2][data_band == index] = color[2]  # Blue
                rgba_band[3][data_band == index] = color[3]  # Alpha

            with rasterio.open(rgb_path, "w", **output_profile) as dst:
                dst.write(rgba_band)
                dst.colorinterp = [
                    ColorInterp.red,
                    ColorInterp.green,
                    ColorInterp.blue,
                    ColorInterp.alpha,
                ]
        else:
            # treat as grayscale image
            alpha_band = dataset.read_masks(1)

            # find scaling factor to RGB values (0 - 255)
            min_value = np.nanmin(data_band)
            max_value = np.nanmax(data_band)
            value_range = max_value - min_value

            if value_range:
                rgb_scale = 255 / value_range
                rgb_offset = 0 - min_value * rgb_scale
                data_band = data_band * rgb_scale + rgb_offset
            else:
                data_band = np.zeros_like(data_band)

            np.nan_to_num(data_band, copy=False)
            data_band = data_band.astype("uint8")

            with rasterio.open(str(rgb_path), mode="w", **output_profile) as dst:
                dst.write(data_band, 1)
                dst.write(data_band, 2)
                dst.write(data_band, 3)
                dst.write(alpha_band, 4)
                dst.colorinterp = [
                    ColorInterp.red,
                    ColorInterp.green,
                    ColorInterp.blue,
                    ColorInterp.alpha,
                ]

        return rgb_path


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

    hazards_names = ArrayField(
        models.CharField(max_length=100, blank=True),
        null=True,
        blank=True,
        verbose_name=_("hazards names"),
        default=list,
        editable=False,
    )

    hazards_codes = ArrayField(
        models.CharField(max_length=100, blank=True),
        null=True,
        blank=True,
        verbose_name=_("hazards codes"),
        default=list,
        editable=False,
    )

    population_exposed = models.PositiveIntegerField(_("population exposed"), blank=True, null=True)
    population_exposed_percent = models.FloatField(_("population exposed (percentage)"), blank=True, null=True)

    population_exposed_ev = models.PositiveIntegerField(
        _("economically vulnerable population exposed"),
        blank=True,
        null=True,
    )
    population_exposed_ev_percent = models.FloatField(
        _("economically vulnerable population exposed (percentage)"),
        blank=True,
        null=True,
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

    def save(self, *args, **kwargs):
        self.set_population_percents()
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        # NOTE: display name based in hazards (as below) is disabled  because was causing maximum
        # recursion error with django-import-export
        # return ", ".join([hazard.name for hazard in self.hazards.all()])
        return _("Hazard Exposure %(uuid)s") % {"uuid": self.uuid}

    @cached_property
    def hazards_names_display(self):
        return ", ".join(self.hazards_names)

    @cached_property
    def administrative_area(self):
        if not self.coverage:
            return None

        return self.coverage.administrative_area

    @cached_property
    def administrative_area_name(self):
        if not self.administrative_area:
            return None

        return self.administrative_area.name

    def get_hazards_names(self):
        return list(self.hazards.values_list("name", flat=True).order_by("name"))

    def set_hazards_names(self):
        self.hazards_names = self.get_hazards_names()

    def get_hazards_codes(self):
        return list(self.hazards.values_list("code", flat=True).order_by("code"))

    def set_hazards_codes(self):
        self.hazards_codes = self.get_hazards_codes()

    def update_hazards_fields(self):
        """Updates object's cached hazards fields in the database"""
        hazards_names = self.get_hazards_names()
        hazards_codes = self.get_hazards_codes()
        type(self).objects.filter(pk=self.pk).update(
            hazards_names=hazards_names,
            hazards_codes=hazards_codes,
            updated_at=Now(),
        )

    def set_population_percents(self):
        if not self.administrative_area:
            return

        total_population = self.administrative_area.population
        if total_population:

            if self.population_exposed is not None:
                self.population_exposed_percent = self.population_exposed / total_population * 100

            if self.population_exposed_ev is not None:
                self.population_exposed_ev_percent = self.population_exposed_ev / total_population * 100
