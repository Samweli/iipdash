"""
Infrastructure models.

This module defines a :class:`OpticalFibre` and :class:`CellTower` models,
which represents optical fibre networks and cellular towers.

References:
    - :class:`django.contrib.gis.db.models.MultiLineStringField`
    - :class:`django.contrib.gis.db.models.PointField`
    - :class:`django_countries.fields.CountryField`

See Also:
    - https://github.com/SmileyChris/django-countries/
    - https://docs.djangoproject.com/en/stable/ref/contrib/gis/

"""

import uuid
from typing import Any, Dict, Tuple

from django.contrib.gis import geos
from django.contrib.gis.db import models
from django.core.validators import MinValueValidator
from django.db.models.functions import Now
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField


class OpticalFibre(models.Model):
    """An optical fibre network.

    It represents an optical fibre network country, spatial geometry,
    and additional information.

    Attributes:
        id (:class:`django.db.models.BigAutoField`):
            A database primary key for the optical fibre network. Inherited
            from :class:`django.db.models.Model`.

        uuid (:class:`django.db.models.UUIDField`):
            A universally unique identifier (UUID) for the optical fibre
            network, generated using :func:`uuid.uuid4`. This field is
            non-editable, unique, and set by default.

        country (:class:`django_countries.fields.CountryField`):
            The country to which the optical fibre network belongs.

        name (:class:`django.db.models.CharField`):
            A human-readable name of the optical fibre network.

        description (:class:`django.db.models.TextField`):
            A long-form description of the optical fibre network.

        geometry (:class:`django.contrib.gis.db.models.MultiPolygonField`):
            The spatial/geometric shape of the optical fibre network.

        created_at (:class:`django.db.models.DateTimeField`):
            The database level timestamp of when the optical fibre network was
            created.

        updated_at (:class:`django.db.models.DateTimeField`):
            The database level timestamp of when the optical fibre network was
            latest modified.

        extras (:class:`django.db.models.JSONField`):
            Additional arbitrary data related to the optical fibre network.

    """

    #: A universally unique identifier (UUID) for the optical fibre network.
    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    #: The country to which the optical fibre network belongs.
    country = CountryField(_("country"), blank=True, db_index=True)

    #: A human-readable name of the optical fibre network.
    name = models.CharField(_("name"), max_length=255, blank=True)

    #: A long-form description of the optical fibre network.
    description = models.TextField(_("description"), blank=True)

    #: The spatial/geometric shape of the optical fibre network.
    geometry = models.MultiLineStringField(
        _("geometry"),
        geography=True,
        blank=True,
        null=True,
        srid=4326,
    )

    #: The database level timestamp of when the optical fibre network was
    #: created.
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        db_default=Now(),
        db_index=True,
    )

    #: The database level timestamp of when the optical fibre network was
    #: latest modified.
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        null=True,
        blank=True,
    )

    #: Additional arbitrary data related to the optical fibre network.
    extras = models.JSONField(_("extras"), blank=True, default=dict)

    class Meta:
        """
        Meta options for the :class:`OpticalFibre` model.

        Attributes:
            verbose_name (str):
                The human-readable name for a single optical fibre network.

            verbose_name_plural (str):
                The human-readable name for multiple optical fibre network.
        """

        verbose_name = _("Optical Fibre Network")
        verbose_name_plural = _("Optical Fibre Networks")

    def save(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> None:
        """
        Save the current optical fibre network instance.

        It ensures the optical fibre network geometry field is stored as a
        :class:`django.contrib.gis.geos.MultiLineString`. If the geometry is
        provided as a single :class:`django.contrib.gis.geos.LineString`, it
        is automatically converted to a
        :class:`django.contrib.gis.geos.MultiLineString` before saving. This
        ensures consistency when handling optical fibre network geometry
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

    def __str__(self):
        """
        Returns the string representation of the optical fibre network.

        Returns:
            str:
                The name of the optical fibre network, or a formatted string
                with the country and UUID.
        """
        return self.name or format_lazy(
            "Optical Fibre: {country}: {uuid}",
            country=self.country,
            uuid=self.uuid,
        )


class CellTower(models.Model):
    """A cell tower.

    It represents a cellular tower country, spatial location, coverage, and
    additional information.

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

        geometry (:class:`django.contrib.gis.db.models.MultiPolygonField`):
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
    )

    #: The network type of the cell tower e.g., GSM, UMTS, LTE, CDMA.
    network_type = models.CharField(
        _("network type"),
        max_length=255,
        blank=True,
        help_text=_("Examples; GSM, UMTS, LTE or CDMA."),
    )

    #: The mobile country code of the cell tower. e.g., 650 for Malawi.
    mcc = models.SmallIntegerField(
        _("mobile country code"),
        blank=True,
        null=True,
        help_text=_("Example 650 for Malawi"),
    )

    #: The spatial location of the cell tower.
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

    #: The estimated coverage range in meters of the cell tower.
    range = models.FloatField(
        _("range (meters)"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=_("Estimate of cell range"),
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
    )

    #: The data source level timestamp of when the cell tower was created.
    src_created = models.DateTimeField(
        _("source record created at"),
        null=True,
        blank=True,
    )

    #: The data source level timestamp of when the cell tower was latest
    #: modified.
    src_updated_at = models.DateTimeField(
        _("source record updated at"),
        null=True,
        blank=True,
    )

    #: The database level timestamp of when the cell tower was created.
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        db_default=Now(),
        db_index=True,
    )

    #: The database level timestamp of when the cell tower was latest
    #: modified.
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        null=True,
        blank=True,
    )

    #: Additional arbitrary data related to the cell tower.
    extras = models.JSONField(_("extras"), blank=True, default=dict)

    class Meta:
        """
        Meta options for the :class:`CellTower` model.

        Attributes:
            verbose_name (str):
                The human-readable name for a single institution.

            verbose_name_plural (str):
                The human-readable name for multiple institutions.
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
        return format_lazy(
            "{network_type} cell tower: {uuid}",
            network_type=self.network_type,
            uuid=self.uuid,
        )

    def __str__(self):
        """
        Returns the string representation of the cell tower.

        Returns:
            str: A user-friendly display name for the cell tower.
        """
        return self.display_name
