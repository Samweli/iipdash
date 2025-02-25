"""
URL configuration for the iipdash project.

The `urlpatterns` list routes URLs to views.

For more information, see the Django documentation:
https://docs.djangoproject.com/en/5.1/topics/http/urls/

Examples:

Function-based views:
    1. Add an import:

       .. code-block:: python

           from my_app import views

    2. Add a URL to urlpatterns:

       .. code-block:: python

           path('', views.home, name='home')

Class-based views:
    1. Add an import:

       .. code-block:: python

           from other_app.views import Home

    2. Add a URL to urlpatterns:

       .. code-block:: python

           path('', Home.as_view(), name='home')

Including another URLconf:
    1. Import the `include()` function:

       .. code-block:: python

           from django.urls import include, path

    2. Add a URL to urlpatterns:

       .. code-block:: python

           path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

from debug_toolbar.toolbar import debug_toolbar_urls
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from . import views
from .api_urls import router as api_router

urlpatterns = [
    path("", TemplateView.as_view(template_name="about/home.html"), name="home"),
    path("maps/", TemplateView.as_view(template_name="about/maps.html"), name="maps"),
    path("about/", TemplateView.as_view(template_name="about/about.html"), name="about"),
    path("education/", views.EducationDashboardView.as_view(), name="education-dashboard"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("api/auth/", include("rest_framework.urls")),
    path("api/oauth/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("api/", include((api_router.urls, "api"))),
    path("openapi/schema/", SpectacularAPIView.as_view(), name="openapi-schema"),
    path("openapi/docs/", SpectacularRedocView.as_view(url_name="openapi-schema"), name="openapi-docs"),
    path("openapi/swagger-ui/", SpectacularSwaggerView.as_view(url_name="openapi-schema"), name="openapi-swagger-ui"),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + debug_toolbar_urls() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.STORAGES["default"]["BACKEND"] == "core.files.ProtectedFileSystemStorage":
    urlpatterns += [path(settings.MEDIA_PROTECTED_URL.lstrip("/"), include("core.media.urls"))]

admin.site.site_header = getattr(settings, "ADMIN_SITE_HEADER", "")
admin.site.index_title = getattr(settings, "ADMIN_INDEX_TITLE", "")
admin.site.site_title = getattr(settings, "ADMIN_SITE_NAME", "")
