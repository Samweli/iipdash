from django.db import transaction
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import HazardExposure


@receiver(m2m_changed, sender=HazardExposure.hazards.through)
def update_exposure_hazards_names(sender, instance, **kwargs):
    transaction.on_commit(lambda: instance.update_hazards_names())
