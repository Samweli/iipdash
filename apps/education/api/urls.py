from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"categories", views.CategoryViewSet, basename="category")
router.register(r"ownerships", views.OwnershipViewSet, basename="ownership")
