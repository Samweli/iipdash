from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"celltowers", views.CellTowerViewSet, basename="celltower")
