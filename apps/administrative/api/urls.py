from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r"areas", views.AreaViewSet, basename="area")

router.register(r"areas-education", views.AreaEducationViewSet, basename="area-education")
router.register(
    r"areas-education-ifond/(?P<distance>\d+)", views.AreaEducationIFONDViewSet, basename="area-education-ifond"
)

router.register(r"areas-mobile-coverage", views.AreaMobileCoverageViewSet, basename="area-mobile-coverage")
router.register(r"areas-internet-speed", views.AreaInternetSpeedViewSet, basename="area-internet-speed")
router.register(r"areas-hazards-exposure", views.AreaHazardExposureViewSet, basename="area-hazard-exposure")
