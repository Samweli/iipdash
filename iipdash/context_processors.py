from django.conf import settings


def site(request):
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_API_NAME": settings.SITE_API_NAME,
        "SITE_API_URL": settings.SITE_API_URL,
    }
