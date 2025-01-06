from rest_framework import routers

from education.api.urls import router as education_router


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
router.include_router(r"education/", education_router)
