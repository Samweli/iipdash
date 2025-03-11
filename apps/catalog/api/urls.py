from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"categories", views.CategoryViewSet, basename="catalog-category")
router.register(r"layers", views.LayerViewSet, basename="catalog-layers")
