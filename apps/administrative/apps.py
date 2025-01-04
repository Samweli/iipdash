"""
Administrative area application configuration.

This module defines the configuration for the `administrative` application by
extending Django's built-in :class:`django.apps.AppConfig` to configure the
app's settings, such as its `name`, `label`, and human-readable `verbose name` etc.

References:
    - :class:`django.apps.AppConfig`
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdministrativeConfig(AppConfig):
    """
    Configuration class for the `administrative` area application.

    This class provides metadata and default settings for the `administrative`
    area app, including its name, default primary key field type, and
    human-readable verbose name.
    """

    #: The default type of primary key field to use for models in this
    #: app. Defaults to :class:`django.db.models.BigAutoField`.
    default_auto_field: str = "django.db.models.BigAutoField"

    #: The full Python path to the application. This is used by Django
    #: to locate the application module.
    name: str = "administrative"

    #: A human-readable name for the application, used in the Django
    #: admin and other parts of the framework.
    verbose_name: str = _("Administrative")
