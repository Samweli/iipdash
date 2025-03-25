import uuid
from pathlib import Path
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models, transaction
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _

from gdal2tiles import gdal2tiles

from .tasks import generate_layer_tiff_tiles


def layer_tiff_path(instance, filename):
    """Returns path for storing mobile coverage tiff files, i.e.
    "infrastructure/mobile-coverage/{instance.uuid}/tiff/{filename}"
    """
    return f"catalog/layers/{instance.uuid}/tiff/{filename}"


class Category(models.Model):
    uuid = models.UUIDField(_("UUID"), default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(_("name"), max_length=255)
    code = models.SlugField(
        _("code"),
        unique=True,
        blank=True,
        null=True,
        max_length=64,
        help_text=_("unique short code that can be used to identify the category"),
    )
    description = models.TextField(_("description"), blank=True)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_default=Now(), blank=True)
    updated_at = models.DateTimeField(
        _("updated at"),
        blank=True,
        null=True,
        auto_now=True,
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Layer(models.Model):
    """A layer"""

    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name="layers",
        related_query_name="layer",
        verbose_name=_("categories"),
    )

    uuid = models.UUIDField(
        _("UUID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    name = models.CharField(_("name"), max_length=255, db_index=True)
    code = models.SlugField(
        _("code"),
        unique=True,
        blank=True,
        null=True,
        max_length=64,
        help_text=_("unique short code that can be used to identify the layer"),
    )
    description = models.TextField(_("description"), blank=True)
    notes = models.TextField(_("notes"), blank=True)

    tags = ArrayField(
        models.CharField(max_length=100, blank=True),
        null=True,
        blank=True,
        verbose_name=_("tags"),
        default=list,
    )

    source = models.TextField(
        _("source"),
        blank=True,
        help_text=_("name of the data source"),
    )
    source_url = models.URLField(
        _("source url"),
        blank=True,
        help_text=_("link of the data source"),
    )
    attribution = models.CharField(_("attribution"), max_length=255, blank=True)
    license = models.TextField(_("license"), blank=True)

    is_public = models.BooleanField(_("is public"), default=False, blank=True)

    tiff = models.FileField(
        _("GeoTIFF"),
        upload_to=layer_tiff_path,
        max_length=510,
        blank=True,
        help_text=_("The tiff file containing the data."),
    )

    created_at = models.DateTimeField(
        _("created at"),
        blank=True,
        db_default=Now(),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        blank=True,
        null=True,
        auto_now=True,
    )

    extras = models.JSONField(_("extras"), blank=True, default=dict)

    class Meta:
        verbose_name = _("Layer")
        verbose_name_plural = _("Layers")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(self.uuid)

        super().save(*args, **kwargs)

        if self.tiff:
            transaction.on_commit(lambda: generate_layer_tiff_tiles.delay(pk=self.pk))

    @property
    def tiles_dir(self):
        if not self.tiff:
            return None

        return Path(f"layers/{self.uuid}/")

    @property
    def tiles_root(self):
        if not self.tiff:
            return None

        return Path(settings.TILES_ROOT) / self.tiles_dir

    @property
    def tms_url(self):
        if not self.tiff:
            return None

        return urljoin(settings.TILES_URL, f"{self.tiles_dir}/{{z}}/{{x}}/{{y}}.png")

    def generate_tiles(self, **kwargs):
        """Generate tiles for using web maps from TIFF file."""

        if not self.tiff:
            return

        kwargs = {
            "webviewer": "none",
            "nb_processes": settings.GDAL2TILES_PROCESSES,
            "profile": "mercator",
            "tile_size": 256,
            "tmscompatible": True,
            "zoom": (1, 15),
            **kwargs,
        }
        gdal2tiles.generate_tiles(self.tiff.path, str(self.tiles_root), **kwargs)
