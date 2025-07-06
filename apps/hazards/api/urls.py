from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"exposure-coverage", views.ExposureCoverageViewSet, basename="exposure-coverage")
