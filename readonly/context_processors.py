from django.conf import settings

def readonly_processor(request):
    return {
        'SITE_READ_ONLY': getattr(settings, 'SITE_READ_ONLY', False),
    }
