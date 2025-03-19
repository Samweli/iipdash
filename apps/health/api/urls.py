from rest_framework import routers

from . import views

router = routers.SimpleRouter()


router.register(r"health-facilities", views.HealthFacilityViewSet, basename="health-facility")
