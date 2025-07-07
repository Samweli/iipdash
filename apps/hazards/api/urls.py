from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"exposure-coverage", views.ExposureCoverageViewSet, basename="exposure-coverage")
router.register(r"hazard-exposures", views.HazardExposureViewSet, basename="hazard-exposure")
