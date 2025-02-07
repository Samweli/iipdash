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
from typing import Any, Dict, Tuple

from django.contrib.gis import geos
from django.contrib.gis.db import models
from django.contrib.gis.gdal import GDALRaster
from django.core.validators import MinValueValidator
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _

from .files import mobile_coverage_tiff_path


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

    #: The adminstrative area to which the cell tower belongs.
    administrative_area = models.ForeignKey(
        "administrative.Area",
        blank=True,
        null=True,
        related_name="infrastructure_cell_towers",
        related_query_name="infrastructure_cell_tower",
        on_delete=models.SET_NULL,
        verbose_name=_("administrative area"),
        help_text=_("The adminstrative area to which the cell tower belongs."),
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

    def __str__(self):
        """
        Returns the string representation of the cell tower.

        Returns:
            str: A user-friendly display name for the cell tower.
        """
        return self.display_name


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
        related_name="infrastructure_mobile_coverages",
        related_query_name="infrastructure_mobile_coverage",
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
    population_covered_percent = models.FloatField(_("population covered percentage"), blank=True, null=True)

    tiff = models.FileField(_("coverage GeoTIFF"), upload_to=mobile_coverage_tiff_path, max_length=510, blank=True)

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
        self.set_raster()
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        return _("%(network_gen)s Mobile Coverage %(area)s") % {
            "network_gen": str(self.network_generation),
            "area": str(self.administrative_area),
        }

    def set_raster(self):
        """Set raster attribute data based on assigned GeoTIFF file."""
        if not self.tiff:
            return

        raster = GDALRaster(self.tiff.read())
        raster_srid = self._meta.model.raster.field.srid

        if raster.srid != raster_srid:
            raster = raster.transform(raster_srid)

        self.raster = raster
