from rest_framework import routers

from education.api.urls import router as education_router

router = routers.DefaultRouter()
router.registry.extend(education_router.registry)
