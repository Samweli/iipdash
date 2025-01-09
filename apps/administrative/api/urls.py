from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"areas", views.AreaViewSet, basename="area")
