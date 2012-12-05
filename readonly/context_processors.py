from django.conf import settings


def readonly(request):
    return {
        'SITE_READ_ONLY': getattr(settings, 'SITE_READ_ONLY', False),
    }
