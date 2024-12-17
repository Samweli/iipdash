import uuid

from django.contrib.gis import geos
from django.contrib.gis.db import models
from django.core.validators import MinValueValidator
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField
from treebeard.mp_tree import MP_Node


class Area(MP_Node):
    """Administrative areas extending :class:`treebeard.mp_tree.MP_Node`."""

    #: A universally unique identifier (UUID).
    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    #: Hierarchy level name e.g ADM1, ADM2 etc.
    type_code = models.SlugField(
        _("area type"),
        blank=True,
        max_length=255,
        db_index=True,
    )

    #: Country under which an area belongs to.
    country = CountryField(_("country"), blank=True, db_index=True)

    #: Human readable name
    name = models.CharField(_("name"), max_length=255)

    #: Unique short code or census code
    code = models.CharField(_("code"), max_length=50, blank=True)

    #: Human readable description/long-form name
    description = models.TextField(_("description"), blank=True)

    #: Human readable full name
    full_name = models.CharField(
        _("full name"),
        max_length=255,
        blank=True,
        help_text=_("automatically generated"),
    )

    #: Total population
    population = models.PositiveIntegerField(
        _("population"),
        blank=True,
        null=True,
    )

    #: Total male population
    population_male = models.PositiveIntegerField(
        _("male population"),
        blank=True,
        null=True,
    )

    #: Total female population
    population_female = models.PositiveIntegerField(
        _("female population"),
        blank=True,
        null=True,
    )

    #: Total population year
    #: Example; 2020
    population_year = models.PositiveIntegerField(
        _("population year"),
        blank=True,
        null=True,
    )

    #: Spatial/Geometric shape
    geometry = models.MultiPolygonField(
        _("geometry"),
        geography=True,
        blank=True,
        null=True,
        srid=4326,
    )

    #: Total area in square meters
    area = models.FloatField(
        _("area (square meters)"),
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )

    #: Database level creation timestamp
    created_at = models.DateTimeField(
        "created at",
        auto_now_add=True,
        db_default=Now(),
    )

    #: Database level latest modification timestamp
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        null=True,
        blank=True,
    )

    #: Extra data
    extras = models.JSONField(_("extras"), blank=True, default=dict)

    #: List of area fields that will be used for node ordering.
    #: Overrides :attr:`treebeard.mp_tree.MP_Node.node_order_by`.
    node_order_by = ["name"]

    class Meta:
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")

    def save(self, *args, **kwargs):
        if self.geometry and isinstance(self.geometry, geos.Polygon):
            self.geometry = geos.MultiPolygon(self.geometry)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
