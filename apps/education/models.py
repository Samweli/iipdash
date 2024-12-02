import uuid

from django.contrib.gis.db import models
from django.db.models.functions import Now
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Category of an educational institution"""

    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    name = models.CharField(_("name"), max_length=255, db_index=True)
    code = models.SlugField(_("code"), blank=True, max_length=50)
    description = models.TextField(_("description"), blank=True)

    created_at = models.DateTimeField("created at", auto_now_add=True, db_default=Now(), db_index=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, null=True, blank=True)
    extras = models.JSONField(_("extras"), blank=True, default=dict)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.name[:50])
        super().save(*args, **kwargs)


class Ownership(models.Model):
    """Ownership type of ana educational institution."""

    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    name = models.CharField(_("name"), max_length=255, db_index=True)
    code = models.SlugField(_("code"), blank=True, max_length=50)
    description = models.TextField(_("description"), blank=True)

    created_at = models.DateTimeField("created at", auto_now_add=True, db_default=Now(), db_index=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, null=True, blank=True)
    extras = models.JSONField(_("extras"), blank=True, default=dict)

    class Meta:
        verbose_name = _("Ownership")
        verbose_name_plural = _("Ownerships")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.name[:50])
        super().save(*args, **kwargs)


class Institution(models.Model):
    """An educational institution."""

    uuid = models.UUIDField(_("UUID"), default=uuid.uuid4, editable=False, unique=True)

    category = models.ForeignKey(
        "Category",
        related_name="institutions",
        related_query_name="institution",
        verbose_name=_("category"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    name = models.CharField(_("name"), max_length=255, db_index=True)

    ownership = models.ForeignKey(
        "Ownership",
        related_name="institutions",
        related_query_name="institution",
        verbose_name=_("ownership"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    description = models.TextField(_("description"), blank=True)
    code = models.CharField(_("code"), max_length=50, blank=True)

    postal_code = models.CharField(_("postal code"), max_length=50, blank=True)

    address = models.CharField(_("address"), max_length=255, blank=True)

    phone = models.CharField(_("phone number"), max_length=50, blank=True)

    fax = models.CharField(_("fax"), max_length=50, blank=True)

    email = models.EmailField(_("email"), blank=True)
    website = models.URLField(_("website"), blank=True, null=True)

    geometry = models.PointField(_("Geometry"), geography=True, blank=True, null=True, srid=4326)

    administrative_area = models.ForeignKey(
        "administrative.Area",
        blank=True,
        null=True,
        related_name="education_institutions",
        related_query_name="education_institution",
        on_delete=models.SET_NULL,
        verbose_name=_("administrative area"),
    )

    osm_id = models.BigIntegerField(_("OSM id"), blank=True, null=True)
    osm_type = models.CharField(_("OSM type"), max_length=255, blank=True)

    created_at = models.DateTimeField("created at", auto_now_add=True, db_default=Now(), db_index=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True, null=True, blank=True)
    extras = models.JSONField(_("extras"), blank=True, default=dict)

    class Meta:
        verbose_name = _("Institution")
        verbose_name_plural = _("Institutions")

    def __str__(self):
        return self.name
