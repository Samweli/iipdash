from django.db import transaction
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import HazardExposure


def _update_exposure_hazards_names(hazard_exposure):
    hazards_names = hazard_exposure.get_hazards_names()
    HazardExposure.objects.filter(pk=hazard_exposure.pk).update(hazards_names=hazards_names)


@receiver(m2m_changed, sender=HazardExposure.hazards.through)
def update_exposure_hazards_names(sender, instance, **kwargs):
    transaction.on_commit(lambda: _update_exposure_hazards_names(instance))
