from rest_framework import routers

from administrative.api.urls import router as administrative_router
from demographics.api.urls import router as demographics_router
from education.api.urls import router as education_router
from infrastructure.api.urls import router as infrastructure_router


class DefaultRouter(routers.DefaultRouter):
    """A custom DefaultRouter which allows adding URLS from other routers with under common prefix"""

    def include_router(self, prefix, router):
        """

        Args
            prefix (str):
                Path prefix for the added URLs

            router (routers.BaseRouter):
                A router instance to be included.
        """
        self.registry.extend([(prefix + url, viewset, basename) for url, viewset, basename in router.registry])


router = DefaultRouter()
router.include_router(r"administrative/", administrative_router)
router.include_router(r"demographics/", demographics_router)
router.include_router(r"education/", education_router)
router.include_router(r"infrastructure/", infrastructure_router)
