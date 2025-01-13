"""
Educational institution models.

This module defines Django models that represent the structure and data
relationships for educational institutions.

References:
    - :class:`django.contrib.gis.db.models.PointField`

See Also:
    - https://docs.djangoproject.com/en/stable/ref/contrib/gis/

"""

import uuid
from typing import Any, Dict, Tuple

from django.contrib.gis.db import models
from django.core.validators import MinValueValidator
from django.db import transaction
from django.db.models.functions import Now
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Category of an educational institution.

    It represents the category an educational institution belongs to,
    e.g., `University` etc.

    Attributes:
        id (:class:`django.db.models.BigAutoField`):
            A database primary key for the category. Inherited from
            :class:`django.db.models.Model`.

        uuid (:class:`django.db.models.UUIDField`):
            A universally unique identifier (UUID) for the category, generated
            using :func:`uuid.uuid4`. This field is non-editable, unique, and set by default.

        name (:class:`django.db.models.CharField`):
            A human-readable name of the category.

        code (:class:`django.db.models.CharField`):
            A unique slugified code for the category, generated automatically
            if not provided.

        description (:class:`django.db.models.TextField`):
            A long-form description of the category.

        created_at (:class:`django.db.models.DateTimeField`):
            The database level timestamp of when the category was created.

        updated_at (:class:`django.db.models.DateTimeField`):
            The database level timestamp of when the category was latest modified.

        extras (:class:`django.db.models.JSONField`):
            Additional arbitrary data related to the category.
    """

    #: A universally unique identifier (UUID) for the category.
    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_("A universally unique identifier (UUID) for the category."),
    )

    #: A human-readable name of the category.
    name = models.CharField(
        _("name"),
        max_length=255,
        db_index=True,
        help_text=_("A human-readable name of the category."),
    )

    #: A unique slugified code for the category, generated automatically
    #: if not provided.
    code = models.SlugField(
        _("code"),
        blank=True,
        max_length=50,
        help_text=_("A unique slugified code for the category."),
    )

    #: A long-form description of the category.
    description = models.TextField(
        _("description"),
        blank=True,
        help_text=_("A long-form description of the category."),
    )

    #: The database level timestamp of when the category was created.
    created_at = models.DateTimeField(
        "created at",
        auto_now_add=True,
        db_default=Now(),
        db_index=True,
        help_text=_("The database level timestamp of when the category was created."),
    )

    #: The database level timestamp of when the category was latest modified.
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        null=True,
        blank=True,
        help_text=_("The database level timestamp of when the category was latest modified."),
    )

    #: Additional arbitrary data related to the category.
    extras = models.JSONField(
        _("extras"),
        blank=True,
        default=dict,
        help_text=_("Additional arbitrary data related to the category."),
    )

    class Meta:
        """
        Meta options for the :class:`Category` model.

        Attributes:
            verbose_name (str):
                The human-readable name for a single category.

            verbose_name_plural (str):
                The human-readable name for multiple categories.
        """

        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        """
        Returns the string representation of the category.

        Returns:
            str: The name of the category.
        """
        return self.name

    def save(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> None:
        """
        Save the current category instance.

        It generates category code if not provided.

        Args:
            *args (Tuple[Any, ...]):
                Positional arguments passed to the parent `save` method.

            **kwargs (Dict[str, Any]):
                Keyword arguments passed to the parent `save` method.

        Returns:
            None
        """
        if not self.code:
            self.code = slugify(self.name[:50])
        super().save(*args, **kwargs)


class Ownership(models.Model):
    """Ownership type of an educational institution.

    It describes the type of ownership for an educational institution,
    e.g., `Public` etc.

    Attributes:
        id (:class:`django.db.models.BigAutoField`):
            A database primary key for the ownership. Inherited from
            :class:`django.db.models.Model`.

        uuid (:class:`django.db.models.UUIDField`):
            A universally unique identifier (UUID) for the ownership, generated
            using :func:`uuid.uuid4`. This field is non-editable, unique, and set by default.

        name (:class:`django.db.models.CharField`):
            A human-readable name of the ownership.

        code (:class:`django.db.models.CharField`):
            A unique slugified code for the ownership, generated automatically
            if not provided.

        description (:class:`django.db.models.TextField`):
            A long-form description of the ownership.

        created_at (:class:`django.db.models.DateTimeField`):
            The database level timestamp of when the ownership was created.

        updated_at (:class:`django.db.models.DateTimeField`):
            The database level timestamp of when the ownership was latest
            modified.

        extras (:class:`django.db.models.JSONField`):
            Additional arbitrary data related to the ownership.

    """

    #: A universally unique identifier (UUID) for the ownership.
    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_("A universally unique identifier (UUID) for the ownership."),
    )

    #:  A human-readable name of the ownership.
    name = models.CharField(
        _("name"),
        max_length=255,
        db_index=True,
        help_text=_("A human-readable name of the ownership."),
    )

    #: A unique slugified code for the ownership, generated automatically
    #: if not provided.
    code = models.SlugField(
        _("code"),
        blank=True,
        max_length=50,
        help_text=_("A unique slugified code for the ownership."),
    )

    #: A long-form description of the ownership.
    description = models.TextField(
        _("description"), blank=True, help_text=_("A long-form description of the ownership.")
    )

    #: The database level timestamp of when the ownership was created.
    created_at = models.DateTimeField(
        "created at",
        auto_now_add=True,
        db_default=Now(),
        db_index=True,
        help_text=_("The database level timestamp of when the ownership was created."),
    )

    #: The database level timestamp of when the ownership was latest
    #: modified.
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        null=True,
        blank=True,
        help_text=_("The database level timestamp of when the ownership was latest modified."),
    )

    #: Additional arbitrary data related to the ownership.
    extras = models.JSONField(
        _("extras"),
        blank=True,
        default=dict,
        help_text=_("Additional arbitrary data related to the ownership."),
    )

    class Meta:
        """
        Meta options for the :class:`Ownership` model.

        Attributes:
            verbose_name (str):
                The human-readable name for a single ownership.

            verbose_name_plural (str):
                The human-readable name for multiple ownerships.
        """

        verbose_name = _("Ownership")
        verbose_name_plural = _("Ownerships")

    def __str__(self):
        """
        Returns the string representation of the ownership.

        Returns:
            str: The name of the ownership.
        """
        return self.name

    def save(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> None:
        """
        Save the current ownership instance.

        It generates ownership code if not provided.

        Args:
            *args (Tuple[Any, ...]):
                Positional arguments passed to the parent `save` method.

            **kwargs (Dict[str, Any]):
                Keyword arguments passed to the parent `save` method.

        Returns:
            None
        """
        if not self.code:
            self.code = slugify(self.name[:50])
        super().save(*args, **kwargs)


class Institution(models.Model):
    """An educational institution.

    It represents an educational institution, with associated category,
    ownership, and additional details.

    Attributes:
        id (:class:`django.db.models.BigAutoField`):
            A database primary key for the institution. Inherited from
            :class:`django.db.models.Model`.

        uuid (:class:`django.db.models.UUIDField`):
            A universally unique identifier (UUID) for the institution, generated
            using :func:`uuid.uuid4`. This field is non-editable, unique, and set by default.

        category (:class:`django.db.models.ForeignKey`):
            The category to which the institution belongs.

        name (:class:`django.db.models.CharField`):
            A human-readable name of the institution.

        ownership (:class:`django.db.models.ForeignKey`):
            The ownership to which the institution belongs.

        description (:class:`django.db.models.TextField`):
            A long-form description of the institution.

        code (:class:`django.db.models.CharField`):
            A unique code for the institution.

        postal_code (CharField):
            A postal code for the institution's address.

        address (:class:`django.db.models.CharField`):
            A physical address of the institution.

        phone (:class:`django.db.models.CharField`):
            A phone number of the institution.

        fax (:class:`django.db.models.CharField`):
            A fax number of the institution.

        email (:class:`django.db.models.EmailField`):
            An email address of the institution.

        website (:class:`django.db.models.URLField`):
            A website URL of the institution.

        geometry (:class:`django.contrib.gis.db.models.PointField`):
            The spatial location of the institution.

        administrative_area (:class:`django.db.models.ForeignKey`):
            The adminstrative area to which the institution belongs.

        has_electricity (:class:`django.db.models.BooleanField`):
            Whether the institution is connected to electricity or not.

        has_fiber_optic (:class:`django.db.models.BooleanField`):
            Whether the institution is connected to fiber optic or not.

        fon_distance (:class:`django.db.models.FloatField`):
            The distance to the nearest fiber optic node (expressed in meters).

        osm_id (:class:`django.db.models.CharField`):
            OpenStreetMap ID of the institution.

        osm_type (:class:`django.db.models.CharField`):
            OpenStreetMap type of the institution.

        created_at (:class:`django.db.models.DateTimeField`):
            The database level timestamp of when the institution was created.

        updated_at (:class:`django.db.models.DateTimeField`):
            The database level timestamp of when the institution was latest
            modified.

        extras (:class:`django.db.models.JSONField`):
            Additional arbitrary data related to the institution.

    """

    #: A universally unique identifier (UUID) for the institution
    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    #: The category to which the institution belongs.
    category = models.ForeignKey(
        "Category",
        related_name="institutions",
        related_query_name="institution",
        verbose_name=_("category"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    #: A human-readable name of the institution.
    name = models.CharField(_("name"), max_length=255, blank=True, db_index=True)

    #: The ownership to which the institution belongs.
    ownership = models.ForeignKey(
        "Ownership",
        related_name="institutions",
        related_query_name="institution",
        verbose_name=_("ownership"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    #: A long-form description of the institution.
    description = models.TextField(_("description"), blank=True)

    #: A unique code for the institution.
    code = models.CharField(_("code"), max_length=50, blank=True)

    #: A postal code for the institution's address.
    postal_code = models.CharField(_("postal code"), max_length=50, blank=True)

    #: A physical address of the institution.
    address = models.CharField(_("address"), max_length=255, blank=True)

    #: A phone number of the institution.
    phone = models.CharField(_("phone number"), max_length=50, blank=True)

    #: A fax number of the institution.
    fax = models.CharField(_("fax"), max_length=50, blank=True)

    #: An email address of the institution.
    email = models.EmailField(_("email"), blank=True)

    #: A website URL of the institution.
    website = models.URLField(_("website"), blank=True, null=True)

    #: The administrative area to which the institution belongs.
    administrative_area = models.ForeignKey(
        "administrative.Area",
        blank=True,
        null=True,
        related_name="education_institutions",
        related_query_name="education_institution",
        on_delete=models.SET_NULL,
        verbose_name=_("administrative area"),
    )

    #: The spatial location of the institution.
    geometry = models.PointField(
        _("location"),
        geography=True,
        blank=True,
        null=True,
        srid=4326,
    )

    #: Whether the institution is connected to electricity or not
    has_electricity = models.BooleanField(_("has electricity"), blank=True, null=True)

    #: Whether the institution is connected to fiber optic or not
    has_fiber_optic = models.BooleanField(_("connected to fiber optic"), blank=True, null=True)

    #: The distance to the nearest fiber optic node (meters).
    fon_distance = models.FloatField(
        _("distance to fiber node"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)],
        help_text=_("distance to the nearest fiber optic node (meters)"),
    )

    #: OpenStreetMap ID of the institution.
    osm_id = models.BigIntegerField(_("OSM id"), blank=True, null=True)

    #: OpenStreetMap type of the institution.
    osm_type = models.CharField(_("OSM type"), max_length=255, blank=True)

    #: The database level timestamp of when the institution was created.
    created_at = models.DateTimeField(
        "created at",
        auto_now_add=True,
        db_default=Now(),
        db_index=True,
    )

    #: The database level timestamp of when the institution was latest
    #: modified.
    updated_at = models.DateTimeField(
        _("updated_at"),
        auto_now=True,
        null=True,
        blank=True,
    )

    #: Additional arbitrary data related to the institution.
    extras = models.JSONField(_("extras"), blank=True, default=dict)

    related_areas = models.ManyToManyField(
        "administrative.Area",
        blank=True,
        editable=False,
        related_name="related_education_institutions",
        related_query_name="related_education_institution",
        verbose_name=_("related administrative areas"),
    )

    class Meta:
        """
        Meta options for the :class:`Institution` model.

        Attributes:
            verbose_name (str):
                The human-readable name for a single institution.

            verbose_name_plural (str):
                The human-readable name for multiple institutions.
        """

        verbose_name = _("Institution")
        verbose_name_plural = _("Institutions")

    def __str__(self):
        """
        Returns the string representation of the institution.

        Returns:
            str: The name of the institution.
        """
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        transaction.on_commit(lambda: self.refresh_related_areas())

    def refresh_related_areas(self):
        """update related areas based on the institution's administrative area"""
        if not self.administrative_area:
            return

        ancestors = self.administrative_area.get_ancestors()
        self.related_areas.clear()
        self.related_areas.add(self.administrative_area, *ancestors)
