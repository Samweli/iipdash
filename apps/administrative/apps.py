from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdministrativeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.administrative"
    verbose_name = _("Administrative")
