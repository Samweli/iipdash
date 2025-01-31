from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"cell-towers", views.CellTowerViewSet, basename="cell-tower")
router.register(r"fiber-optics", views.FiberOpticViewSet, basename="fiber-optic")
