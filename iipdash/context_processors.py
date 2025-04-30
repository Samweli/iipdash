from django.conf import settings
from django.urls import reverse


def site(request):
    return {
        "API_ROOT": request.build_absolute_uri(reverse("api:api-root")),
        "SITE_NAME": settings.SITE_NAME,
        "SITE_URL": settings.SITE_URL,
        "SITE_TAGLINE": settings.SITE_TAGLINE,
        "SITE_API_NAME": settings.SITE_API_NAME,
        "SITE_API_URL": settings.SITE_API_URL,
        "MAPBOX_STYLE_ID": settings.MAPBOX_STYLE_ID,
        "MAPBOX_ACCESS_TOKEN": settings.MAPBOX_ACCESS_TOKEN,
        "BASEMAP_URL": settings.BASEMAP_URL,
        "BASEMAP_ATTRIBUTION": settings.BASEMAP_ATTRIBUTION,
        "MAP_DEFAULT_CENTER": settings.MAP_DEFAULT_CENTER,
        "MAP_DEFAULT_ZOOM": settings.MAP_DEFAULT_ZOOM,
        "MAP_DEFAULT_BBOX": settings.MAP_DEFAULT_BBOX,
        "GOOGLE_ANALYTICS_TAG_ID": settings.GOOGLE_ANALYTICS_TAG_ID,
    }
