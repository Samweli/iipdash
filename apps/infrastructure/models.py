"""
Infrastructure models

This module defines the :class:`FiberOptic` and :class:`CellTower` models,
which represent fiber optic networks and cellular towers.

These models store geographical and operational data for telecommunication
infrastructure, supporting GIS capabilities.

References:
    - :class:`django.contrib.gis.db.models.MultiLineStringField`
    - :class:`django.contrib.gis.db.models.PointField`
    - :class:`django.db.models.Model`

See Also:
    - `Django GIS Documentation <https://docs.djangoproject.com/en/stable/ref/contrib/gis/>`_
"""

import uuid
from pathlib import Path
from typing import Any, Dict, Tuple
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.gis import geos
from django.contrib.gis.db import models
from django.contrib.gis.gdal import GDALRaster
from django.core.validators import MinValueValidator
from django.db import transaction
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _

import gdal2tiles
import numpy as np
import rasterio
from django_countries.fields import CountryField
from rasterio.enums import ColorInterp

from administrative.models import Area

from .files import mobile_coverage_tiff_path
from .tasks import generate_mobile_coverage_tiles, update_mobile_coverage_raster


class FiberOptic(models.Model):
    """A fiber optic network.

    This model stores details about fiber optic networks, including their
    spatial geometry, operational status, and administrative area.

    Attributes:
        id (:class:`django.db.models.BigAutoField`):
            A database primary key for the fiber optic network. Inherited
            from :class:`django.db.models.Model`.

        uuid (:class:`django.db.models.UUIDField`):
            A universally unique identifier (UUID) for the fiber optic
            network, generated using :func:`uuid.uuid4`. This field is
            non-editable, unique, and set by default.

        name (:class:`django.db.models.CharField`):
            A human-readable name of the fiber optic network.

        description (:class:`django.db.models.TextField`):
            A long-form description of the fiber optic network.

        geometry (:class:`django.contrib.gis.db.models.MultiLineStringField`):
            The spatial/geometric shape of the fiber optic network.

        administrative_area (:class:`django.db.models.ForeignKey`):
            The adminstrative area to which the fiber optic network belongs.

        status (:class:`django.db.models.CharField`):
            The operational status of the fiber optic network.

        operator_name (:class:`django.db.models.CharField`):
            The name of the network operator managing the fiber optic network.

        created_at (:class:`django.db.models.DateTimeField`):
            The database level timestamp of when the fiber optic network was
            created.

        updated_at (:class:`django.db.models.DateTimeField`):
            The database level timestamp of when the fiber optic network was
            latest modified.

        extras (:class:`django.db.models.JSONField`):
            Additional arbitrary data related to the fiber optic network.
    """

    class FiberOpticStatus(models.TextChoices):
        """Operational statuses for a fiber optic network."""

        OPERATIONAL = "operational", _("Operational")
        UNDER_CONSTRUCTION = "under-construction", _("Under construction")
        PLANNED = "planned", _("Planned")
        PROPOSED = "proposed", _("Proposed")

    #: A universally unique identifier (UUID) for the fiber optic network.
    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_("A universally unique identifier (UUID) for the fiber optic network"),
    )

    #: A human-readable name of the fiber optic network.
    name = models.CharField(
        _("name"),
        max_length=255,
        blank=True,
        help_text=_("A human-readable name of the fiber optic network."),
    )

    #: A long-form description of the fiber optic network.
    description = models.TextField(
        _("description"),
        blank=True,
        help_text=_("A long-form description of the fiber optic network."),
    )

    #: The spatial/geometric shape of the fiber optic network.
    geometry = models.MultiLineStringField(
        _("geometry"),
        geography=True,
        blank=True,
        null=True,
        srid=4326,
        help_text=_("The spatial/geometric shape of the fiber optic network."),
    )

    #: The adminstrative area to which the fiber optic network belongs.
    administrative_area = models.ForeignKey(
        "administrative.Area",
        blank=True,
        null=True,
        related_name="fiber_optics",
        related_query_name="fiber_optic",
        on_delete=models.SET_NULL,
        verbose_name=_("administrative area"),
        help_text=_("The administrative area to which the fiber optic network belongs."),
    )

    #: The operational status of the fiber optic network.
    status = models.CharField(
        _("status"),
        choices=FiberOpticStatus,
        blank=True,
        max_length=128,
        db_index=True,
        help_text=_("The operational status of the fiber optic network."),
    )

    #: The name of the network operator managing the fiber optic network.
    operator_name = models.CharField(
        _("operator name"),
        blank=True,
        max_length=255,
        help_text=_("The name of the network operator managing the fiber optic network."),
    )

    #: The database level timestamp of when the fiber optic network was
    #: created.
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        db_default=Now(),
        db_index=True,
        help_text=_("The database level timestamp of when the fiber optic network was created."),
    )

    #: The database level timestamp of when the fiber optic network was
    #: latest modified.
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        null=True,
        blank=True,
        help_text=_("The database level timestamp of when the fiber optic network was latest modified."),
    )

    #: Additional arbitrary data related to the fiber optic network.
    extras = models.JSONField(
        _("extras"),
        blank=True,
        default=dict,
        help_text=_("Additional arbitrary data related to the fiber optic network."),
    )

    class Meta:
        """
        Meta options for the :class:`FiberOptic` model.

        Attributes:
            verbose_name (str):
                The human-readable name for a single fiber optic network.

            verbose_name_plural (str):
                The human-readable name for multiple fiber optic network.
        """

        verbose_name = _("Fiber Optic Network")
        verbose_name_plural = _("Fiber Optic Networks")

    def save(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> None:
        """
        Save the current fiber optic network instance.

        It ensures the fiber optic network geometry field is stored as a
        :class:`django.contrib.gis.geos.MultiLineString`. If the geometry is
        provided as a single :class:`django.contrib.gis.geos.LineString`, it
        is automatically converted to a
        :class:`django.contrib.gis.geos.MultiLineString` before saving. This
        ensures consistency when handling fiber optic network geometry
        spatial data.

        Args:
            *args (Tuple[Any, ...]):
                Positional arguments passed to the parent `save` method.

            **kwargs (Dict[str, Any]):
                Keyword arguments passed to the parent `save` method.

        Returns:
            None
        """
        if self.geometry and isinstance(self.geometry, geos.LineString):
            self.geometry = geos.MultiLineString(self.geometry)
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        """
        A user-friendly display name for the optic network.

        Returns:
            str:
                A user-friendly display name.
        """
        if self.name:
            return self.name
        elif self.operator_name:
            return self.operator_name
        elif self.administrative_area and hasattr(self.administrative_area, "country"):
            return _("Fiber Optic: %(country)s: %(uuid)s") % {
                "country": self.administrative_area.country,
                "uuid": self.uuid,
            }
        else:
            return _("Fiber Optic: %(uuid)s") % {
                "uuid": self.uuid,
            }

    def __str__(self):
        """
        Returns the string representation of the fiber optic network.

        Returns:
            str:
                The name of the fiber optic network, or a formatted string
                with the country and UUID.
        """
        return self.name or self.display_name


class FiberOpticNode(models.Model):
    """A Mobile network Node."""

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
        related_name="fiber_optic_nodes",
        related_query_name="fiber_optic_node",
        on_delete=models.SET_NULL,
        verbose_name=_("administrative area"),
    )

    node_type = models.CharField(_("node type"), max_length=255, blank=True, null=True, db_index=True)

    #: Spatial location of the fiber node.
    geometry = models.PointField(
        _("location"),
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

    extras = models.JSONField(
        _("extras"),
        blank=True,
        default=dict,
    )

    class Meta:
        verbose_name = _("Fiber Optic Node")
        verbose_name_plural = _("Fiber Optic Nodes")

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        self.set_administrative_area()
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        if self.node_type:
            return f"{self.node_type}: {self.administrative_area}"
        else:
            return _("fiber optic node: %(administrative_area)s") % {
                "administrative_area": str(self.administrative_area)
            }

    def set_administrative_area(self):
        """Try to detect related administrative area based on the location if not yet provided."""
        if self.administrative_area is not None or self.geometry is None:
            return

        area = Area.objects.filter(geometry__covers=self.geometry).order_by("-depth").first()
        if area:
            self.administrative_area = area


class NetworkGeneration(models.Model):
    """A mobile network generation."""

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
        verbose_name = _("Mobile Network Generation")
        verbose_name_plural = _("Mobile Network Generations")

    def __str__(self):
        return self.name


class CellTower(models.Model):
    """A cellular tower.

    This model stores details about cellular towers, including their
    spatial geometry, network type, coverage range, and administrative area.

    Attributes:
        id (:class:`django.db.models.BigAutoField`):
            A database primary key for the cell tower. Inherited from
            :class:`django.db.models.Model`.

        uuid (:class:`django.db.models.UUIDField`):
            A universally unique identifier (UUID) for the cell tower,
            generated using :func:`uuid.uuid4`. This field is non-editable,
            unique, and set by default.

        network_type (:class:`django.db.models.CharField`):
            The network type of the cell tower e.g., GSM, UMTS, LTE, CDMA.

        mcc (:class:`django.db.models.SmallIntegerField`):
            The mobile country code of the cell tower. e.g., 650 for Malawi.

        geometry (:class:`django.contrib.gis.db.models.PointField`):
            The spatial location of the cell tower.

        location_is_approximate (:class:`django.db.models.BooleanField`):
            Defines if coordinates of the cell tower are exact or approximate.

        range (:class:`django.db.models.FloatField`):
            The estimated coverage range in meters of the cell tower.

        administrative_area (:class:`django.db.models.ForeignKey`):
            The adminstrative area to which the cell tower belongs.

        src_created_at (:class:`django.db.models.DateTimeField`):
            The data source level timestamp of when the cell tower was created.

        src_updated_at (:class:`django.db.models.DateTimeField`):
            The data source level timestamp of when the cell tower was latest
            modified.

        created_at (:class:`django.db.models.DateTimeField`):
            The database level timestamp of when the cell tower was created.

        updated_at (:class:`django.db.models.DateTimeField`):
            The database level timestamp of when the cell tower was latest
            modified.

        extras (:class:`django.db.models.JSONField`):
            Additional arbitrary data related to the cell tower.
    """

    #: A universally unique identifier (UUID) for the cell tower.
    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_("A universally unique identifier (UUID) for the cell tower."),
    )

    #: The network type of the cell tower e.g., GSM, UMTS, LTE, CDMA.
    network_type = models.CharField(
        _("network type"),
        max_length=255,
        blank=True,
        help_text=_("The network type of the cell tower e.g., GSM, UMTS, LTE, CDMA."),
    )

    #: The mobile country code of the cell tower. e.g., 650 for Malawi.
    mcc = models.SmallIntegerField(
        _("mobile country code"),
        blank=True,
        null=True,
        help_text=_("The mobile country code of the cell tower. e.g., 650 for Malawi."),
    )

    #: The spatial location of the cell tower.
    geometry = models.PointField(
        _("location"),
        geography=True,
        blank=True,
        null=True,
        srid=4326,
        help_text=_("The spatial location of the cell tower."),
    )

    #: Defines if coordinates of the cell tower are exact or approximate.
    location_is_approximate = models.BooleanField(
        _("location is approximate"),
        blank=True,
        null=True,
        help_text=_("Defines if coordinates of the cell tower are exact or approximate."),
    )

    #: The estimated coverage range in meters of the cell tower.
    range = models.FloatField(
        _("range (meters)"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=_("The estimated coverage range in meters of the cell tower."),
    )

    #: The administrative area to which the cell tower belongs.
    administrative_area = models.ForeignKey(
        "administrative.Area",
        blank=True,
        null=True,
        related_name="cell_towers",
        related_query_name="cell_tower",
        on_delete=models.SET_NULL,
        verbose_name=_("administrative area"),
        help_text=_("The administrative area to which the cell tower belongs."),
    )

    #: The data source level timestamp of when the cell tower was created.
    src_created_at = models.DateTimeField(
        _("source record created at"),
        null=True,
        blank=True,
        help_text=_("The data source level timestamp of when the cell tower was created."),
    )

    #: The data source level timestamp of when the cell tower was latest
    #: modified.
    src_updated_at = models.DateTimeField(
        _("source record updated at"),
        null=True,
        blank=True,
        help_text=_("The data source level timestamp of when the cell tower was latest modified."),
    )

    #: The database level timestamp of when the cell tower was created.
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        db_default=Now(),
        db_index=True,
        help_text=_("The database level timestamp of when the cell tower was created."),
    )

    #: The database level timestamp of when the cell tower was latest
    #: modified.
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        null=True,
        blank=True,
        help_text=_("The database level timestamp of when the cell tower was latest modified."),
    )

    #: Additional arbitrary data related to the cell tower.
    extras = models.JSONField(
        _("extras"),
        blank=True,
        default=dict,
        help_text=_("Additional arbitrary data related to the cell tower."),
    )

    class Meta:
        """
        Meta options for the :class:`CellTower` model.

        Attributes:
            verbose_name (str):
                The human-readable name for a single cell tower.

            verbose_name_plural (str):
                The human-readable name for multiple cell towers.
        """

        verbose_name = _("Cell Tower")
        verbose_name_plural = _("Cell Towers")

    def __str__(self):
        """
        Returns the string representation of the cell tower.

        Returns:
            str: A user-friendly display name for the cell tower.
        """
        return self.display_name

    def save(self, *args, **kwargs):
        self.set_administrative_area()
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        """
        A user-friendly display name for the cell tower.

        Returns:
            str:
                A user-friendly display name.
        """
        return _("%(network_type)s cell tower: %(uuid)s") % {
            "network_type": self.network_type,
            "uuid": self.uuid,
        }

    def set_administrative_area(self):
        """Try to detect related administrative area based on the location if not yet provided."""
        if self.administrative_area is not None or self.geometry is None:
            return

        area = Area.objects.filter(geometry__covers=self.geometry).order_by("-depth").first()
        if area:
            self.administrative_area = area


class MobileCoverage(models.Model):
    """Mobile network coverage information per administrative area."""

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
        related_name="mobile_coverages",
        related_query_name="mobile_coverage",
        on_delete=models.SET_NULL,
        verbose_name=_("administrative area"),
    )

    #: The mobile network generation e.g., 2G, 3G, 4G, 5G.
    network_generation = models.ForeignKey(
        NetworkGeneration,
        related_name="mobile_coverages",
        related_query_name="mobile_coverage",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("mobile network generation"),
    )

    population_covered = models.PositiveIntegerField(_("population covered"), blank=True, null=True)
    population_covered_percent = models.FloatField(_("population covered (percentage)"), blank=True, null=True)

    population_uncovered = models.PositiveIntegerField(_("population not covered"), blank=True, null=True)
    population_uncovered_percent = models.FloatField(_("population not covered (percentage)"), blank=True, null=True)

    tiff = models.FileField(
        _("coverage GeoTIFF"),
        upload_to=mobile_coverage_tiff_path,
        max_length=510,
        blank=True,
        help_text=_("The file is expected to contain one band."),
    )

    #: PostGIS raster
    raster = models.RasterField(
        _("coverage raster"),
        srid=4326,
        blank=True,
        null=True,
        editable=False,
        help_text=_("coverage raster data stored in the database."),
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
        verbose_name = _("Mobile Coverage")
        verbose_name_plural = _("Mobile Coverages")
        constraints = [
            models.UniqueConstraint(
                fields=["administrative_area", "network_generation"],
                name="%(app_label)s_%(class)s_administrative_area_network_generation",
            )
        ]

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        transaction.on_commit(self.auto_process_tiff)

    @property
    def display_name(self):
        return _("%(network_gen)s Mobile Coverage %(area)s") % {
            "network_gen": str(self.network_generation),
            "area": str(self.administrative_area),
        }

    @property
    def tiles_dir(self):
        return Path(f"mobile-coverage/{self.uuid}/")

    @property
    def tiles_root(self):
        return Path(settings.TILES_ROOT) / self.tiles_dir

    @property
    def tms_url(self):
        if not self.tiff:
            return None

        return urljoin(settings.TILES_URL, f"{self.tiles_dir}/{{z}}/{{x}}/{{y}}.png")

    def auto_process_tiff(self):
        """Process the TIFF in the background.

        This involves
         - Ingesting the raster data into the database (if the tiff file is less than ~10MB).
         - Generation of raster tiles for utilization in various applications (if the tiff file is less than ~20MB)
        """
        if not self.tiff:
            return

        if self.tiff.size <= 10000000:
            update_mobile_coverage_raster.delay(pk=self.pk)

        if self.tiff.size <= 20000000:
            generate_mobile_coverage_tiles.delay(pk=self.pk)

    def set_raster(self):
        """Set raster attribute data based on assigned GeoTIFF file."""
        if not self.tiff:
            return

        raster = GDALRaster(self.tiff.read())
        raster_srid = self._meta.model.raster.field.srid

        if raster.srid != raster_srid:
            raster = raster.transform(raster_srid)

        self.raster = raster

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
        gdal2tiles.generate_tiles(str(rgb_tiff), str(self.tiles_root), **kwargs)

    def band2rgba(self):
        """Converts a single band coverage GeoTIFF to RGBA format.

        Returns:
            Path: Path to the created RGBA GeoTIFF file.
        """
        dataset = rasterio.open(self.tiff.open())
        data_band = dataset.read(1)

        og_file_name = Path(self.tiff.name).name
        rgb_rel_path = f"infrastructure/mobile-coverage/{self.uuid}/tiff-rgba/{og_file_name}"
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

            colormap.update(
                {
                    0: (0, 0, 0, 255),
                    1: (0, 0, 0, 90),
                    2: (0, 0, 0, 50),
                    3: (0, 0, 0, 0),
                }
            )

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


class InternetSpeed(models.Model):
    """Internet information per administrative area."""

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
        related_name="internet_speeds",
        related_query_name="internet_speed",
        on_delete=models.SET_NULL,
        verbose_name=_("administrative area"),
    )

    mobile_speed = models.FloatField(_("mobile speed (Mbps)"), blank=True, null=True)
    fixed_speed = models.FloatField(_("fixed speed (Mbps)"), blank=True, null=True)

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
        verbose_name = _("Internet Speed")
        verbose_name_plural = _("Internet Speeds")

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        return _("%(area)s internet speed") % {
            "area": str(self.administrative_area),
        }


class ElectricityNetwork(models.Model):
    """Electricity network"""

    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_("A universally unique identifier (UUID)"),
    )

    voltage_kv = models.PositiveIntegerField(_("voltage KV"), blank=True, null=True)
    status = models.CharField(_("status"), max_length=255, blank=True)
    source = models.CharField(_("source"), max_length=255, blank=True)
    from_nm = models.CharField(_("from nm"), max_length=255, blank=True)
    to_nm = models.CharField(_("to nm"), max_length=255, blank=True)
    network_type = models.CharField(_("network type"), max_length=255, blank=True)

    country = CountryField(_("country"), blank=True)

    geometry = models.MultiLineStringField(
        _("geometry"),
        geography=True,
        blank=True,
        null=True,
        srid=4326,
    )

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
        verbose_name = _("Electricity Network")
        verbose_name_plural = _("Electricity Networks")

    def __str__(self):
        return f"{self.country}: {self.from_nm} - {self.to_nm}"
