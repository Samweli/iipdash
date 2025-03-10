"""
Administrative Area models.

This module defines an :class:`Area` model, which represents administrative
areas hierarchy. It uses :class:`treebeard.mp_tree.MP_Node` for hierarchical
structure and :class:`django.contrib.gis.db.models.MultiPolygonField` for
spatial/geometric fields for geographic representation.

References:
    - :class:`treebeard.mp_tree.MP_Node`
    - :class:`django.contrib.gis.db.models.MultiPolygonField`

See Also:
    - https://django-treebeard.readthedocs.io/en/latest/
    - https://github.com/SmileyChris/django-countries/
    - https://docs.djangoproject.com/en/stable/ref/contrib/gis/

"""

import uuid
from typing import Any, Dict, Tuple

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Area
from django.contrib.gis.geos import MultiPolygon, Polygon
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField
from treebeard.mp_tree import MP_Node


class Area(MP_Node):
    """
    Administrative area model extending :class:`treebeard.mp_tree.MP_Node`.

    This model stores administrative areas in a hierarchical structure and
    provides a way to manage and represent country administrative areas
    e.g. `states`, `provinces`, `regions`, `districts` etc.

    Attributes:
        id (:class:`django.db.models.BigAutoField`):
            A database primary key for the area. Inherited from
            :class:`django.db.models.Model`.

        uuid (:class:`django.db.models.UUIDField`):
            A universally unique identifier (UUID) for the area, generated
            using :func:`uuid.uuid4`. This field is non-editable, unique, and set by default.

        type_code (:class:`django.db.models.SlugField`):
            A hierarchy level name of the area, e.g., `province`, `district`, etc.

        country (:class:`django_countries.fields.CountryField`):
            The country to which the area belongs.

        name (:class:`django.db.models.CharField`):
            A human-readable name of the area.

        code (:class:`django.db.models.CharField`):
            A unique short code or census code of the area.

        description (:class:`django.db.models.TextField`):
            A long-form description of the area.

        full_name (:class:`django.db.models.CharField`):
            The full name of the area, automatically generated.

        population (:class:`django.db.models.PositiveIntegerField`):
            The total population of the area.

        population_male (:class:`django.db.models.PositiveIntegerField`):
            The male population of the area.

        population_female (:class:`django.db.models.PositiveIntegerField`):
            The female population of the area.

        population_year (:class:`django.db.models.PositiveIntegerField`):
            The year for the population data e.g., `2020`.

        geometry (:class:`django.contrib.gis.db.models.MultiPolygonField`):
            The spatial/geometric shape of the area.

        area (:class:`django.db.models.FloatField`):
            The total area of the `area` in square meters.

        created_at (:class:`django.db.models.DateTimeField`):
            The database level timestamp of when the area was created.

        updated_at (:class:`django.db.models.DateTimeField`):
            The database level timestamp of when the area was latest modified.

        extras (:class:`django.db.models.JSONField`):
            Additional arbitrary data related to the area.

        node_order_by (list[str]):
            List of area fields that will be used for hierarchy ordering.
            It overrides :attr:`treebeard.mp_tree.MP_Node.node_order_by`.
    """

    #: A universally unique identifier (UUID) for the area.
    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_("A universally unique identifier (UUID) for the area."),
    )

    #: A hierarchy level name of the area, e.g., `province`, `district`, etc.
    type_code = models.SlugField(
        _("area type"),
        blank=True,
        max_length=255,
        db_index=True,
        help_text=_("A hierarchy level name of the area, e.g., `province`, `district`, etc."),
    )

    #: The country to which the area belongs.
    country = CountryField(
        _("country"),
        blank=True,
        db_index=True,
        help_text=_("The country to which the area belongs."),
    )

    #: A human-readable name of the area.
    name = models.CharField(
        _("name"),
        max_length=255,
        help_text=_("A human-readable name of the area."),
    )

    #: A unique short code or census code of the area.
    code = models.CharField(
        _("code"),
        max_length=50,
        blank=True,
        help_text=_("A unique short code or census code of the area."),
    )

    #: A long-form description of the area.
    description = models.TextField(
        _("description"),
        blank=True,
        help_text=_("A long-form description of the area."),
    )

    #: The full name of the area, automatically generated.
    full_name = models.CharField(
        _("full name"),
        max_length=255,
        blank=True,
        help_text=_("The full name of the area, automatically generated."),
    )

    #: The total population of the area.
    population = models.PositiveIntegerField(
        _("population"),
        blank=True,
        null=True,
        help_text=_("The total population of the area."),
    )

    #: The male population of the area.
    population_male = models.PositiveIntegerField(
        _("male population"),
        blank=True,
        null=True,
        help_text=_("The male population of the area."),
    )

    #: The female population of the area.
    population_female = models.PositiveIntegerField(
        _("female population"),
        blank=True,
        null=True,
        help_text=_("The female population of the area."),
    )

    #: The year for the population data e.g., 2020.
    population_year = models.PositiveIntegerField(
        _("population year"),
        blank=True,
        null=True,
        help_text=_("The year for the population data e.g., 2020."),
    )

    #: The spatial/geometric shape of the area.
    geometry = models.MultiPolygonField(
        _("geometry"),
        geography=True,
        blank=True,
        null=True,
        srid=4326,
        help_text=_("The spatial/geometric shape of the area."),
    )

    #: A version of geometry optimized for performant rendering.
    geom = models.MultiPolygonField(
        _("geom"),
        geography=False,
        blank=True,
        null=True,
        srid=3857,
        editable=False,
        help_text=_("A version of geometry optimized for performant rendering."),
    )

    #: The total area of the `area` in square meters.
    area = models.GeneratedField(
        expression=Area("geometry"),
        output_field=models.FloatField(null=True),
        db_persist=True,
        blank=True,
        null=True,
        verbose_name=_("area (square meters)"),
        help_text=_("The calculated total area of the `area` in square meters."),
    )

    #: The database level timestamp of when the area was created.
    created_at = models.DateTimeField(
        "created at",
        auto_now_add=True,
        db_default=Now(),
        help_text=_("The database level timestamp of when the area was created."),
    )

    #: The database level timestamp of when the area was latest modified.
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        null=True,
        blank=True,
        help_text=_("The database level timestamp of when the area was latest modified."),
    )

    #: Additional arbitrary data related to the area.
    extras = models.JSONField(
        _("extras"),
        blank=True,
        default=dict,
        help_text=_("Additional arbitrary data related to the area."),
    )

    #: List of area fields that will be used for hierarchy ordering.
    #: It overrides :attr:`treebeard.mp_tree.MP_Node.node_order_by`.
    node_order_by = ["name"]

    class Meta:
        """
        Meta options for the :class:`Area` model.

        Attributes:
            verbose_name (str):
                The human-readable name for a single area.

            verbose_name_plural (str):
                The human-readable name for multiple areas.
        """

        verbose_name = _("Area")
        verbose_name_plural = _("Areas")

    def save(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> None:
        """
        Save the current area instance.

        It ensures the area geometry field is stored as a :class:`django.contrib.gis.geos.MultiPolygon`.
        If the geometry is provided as a single :class:`django.contrib.gis.geos.Polygon`,
        it is automatically converted to a :class:`django.contrib.gis.geos.MultiPolygon`
        before saving. This ensures consistency when handling area geometry
        spatial data.

        Args:
            *args (Tuple[Any, ...]):
                Positional arguments passed to the parent `save` method.

            **kwargs (Dict[str, Any]):
                Keyword arguments passed to the parent `save` method.

        Returns:
            None
        """

        if isinstance(self.geometry, Polygon):
            self.geometry = MultiPolygon(self.geometry)

        self.geom = self.geometry2geom()

        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns the string representation of the area.

        Returns:
            str: The name of the area.
        """
        return self.name

    def geometry2geom(self):
        """Transform geometry to simplified EPSG:3857"""

        if self.geometry:
            tolerance = settings.ADMINISTRATIVE_AREAS_SIMPLIFICATION_TOLERANCE
            geom = self.geometry.transform(3857, clone=True)
            geom = geom.simplify(tolerance, preserve_topology=True)

            if isinstance(geom, Polygon):
                geom = MultiPolygon(geom)

            return geom


class PopulationDensityHD(models.Model):
    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_("A universally unique identifier (UUID) for the area."),
    )

    administrative_area = models.ForeignKey(
        "Area",
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
        help_text=_("The spatial location of the institution."),
    )

    population_density = models.FloatField(
        _("population density"),
        help_text=_("population in 1-arc-second-by-1-arc-second grid (30.87-meter-by-30.87 at the equator)"),
        db_index=True,
    )

    year = models.PositiveIntegerField(_("year"), blank=True, null=True)

    class Meta:
        verbose_name = _("Population Density (HD)")
        verbose_name_plural = _("Population Densities (HD)")
        indexes = [
            models.Index(fields=["administrative_area", "population_density"], name="admin_area_pop_density_idx"),
        ]
