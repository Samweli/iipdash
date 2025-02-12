from django.conf import settings


def site(request):
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_TAGLINE": settings.SITE_TAGLINE,
        "SITE_API_NAME": settings.SITE_API_NAME,
        "SITE_API_URL": settings.SITE_API_URL,
        "MAPBOX_STYLE_ID": settings.MAPBOX_STYLE_ID,
        "MAPBOX_ACCESS_TOKEN": settings.MAPBOX_ACCESS_TOKEN,
    }
