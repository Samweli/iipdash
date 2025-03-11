from rest_framework import routers

from . import views

router = routers.SimpleRouter()


router.register(r"population-density-hd", views.PopulationDensityHDViewSet, basename="population-density-hd")
