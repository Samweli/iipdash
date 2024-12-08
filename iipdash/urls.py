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
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]

admin.site.site_header = getattr(settings, "ADMIN_SITE_HEADER", "")
admin.site.index_title = getattr(settings, "ADMIN_INDEX_TITLE", "")
admin.site.site_title = getattr(settings, "ADMIN_SITE_NAME", "")
