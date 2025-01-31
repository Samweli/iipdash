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
from django.contrib.gis.geos import MultiPolygon, Polygon
from django.core.validators import MinValueValidator
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField
from treebeard.mp_tree import MP_Node


class Area(MP_Node):
    """
    Administrative area model extending :class:`treebeard.mp_tree.MP_Node`.

    It represents administrative areas in a hierarchical structure and
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
            A hierarchy level name of the area, e.g., `ADM1`, `ADM2`, etc.

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
    )

    #: A hierarchy level name of the area, e.g., `ADM1`, `ADM2`, etc.
    type_code = models.SlugField(
        _("area type"),
        blank=True,
        max_length=255,
        db_index=True,
    )

    #: The country to which the area belongs.
    country = CountryField(_("country"), blank=True, db_index=True)

    #: A human-readable name of the area.
    name = models.CharField(_("name"), max_length=255)

    #: A unique short code or census code of the area.
    code = models.CharField(_("code"), max_length=50, blank=True)

    #: A long-form description of the area.
    description = models.TextField(_("description"), blank=True)

    #: The full name of the area, automatically generated.
    full_name = models.CharField(
        _("full name"),
        max_length=255,
        blank=True,
        help_text=_("automatically generated"),
    )

    #: The total population of the area.
    population = models.PositiveIntegerField(
        _("population"),
        blank=True,
        null=True,
    )

    #: The male population of the area.
    population_male = models.PositiveIntegerField(
        _("male population"),
        blank=True,
        null=True,
    )

    #: The female population of the area.
    population_female = models.PositiveIntegerField(
        _("female population"),
        blank=True,
        null=True,
    )

    #: The year for the population data e.g., 2020.
    population_year = models.PositiveIntegerField(
        _("population year"),
        blank=True,
        null=True,
    )

    #: The spatial/geometric shape of the area.
    geometry = models.MultiPolygonField(
        _("geometry"),
        geography=True,
        blank=True,
        null=True,
        srid=4326,
    )

    #: A version of geometry optimized for performant rendering.
    geom = models.MultiPolygonField(_("geom"), geography=False, blank=True, null=True, srid=3857, editable=False)

    #: The total area of the `area` in square meters.
    area = models.FloatField(
        _("area (square meters)"),
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )

    #: The database level timestamp of when the area was created.
    created_at = models.DateTimeField(
        "created at",
        auto_now_add=True,
        db_default=Now(),
    )

    #: The database level timestamp of when the area was latest modified.
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        null=True,
        blank=True,
    )

    #: Additional arbitrary data related to the area.
    extras = models.JSONField(_("extras"), blank=True, default=dict)

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
