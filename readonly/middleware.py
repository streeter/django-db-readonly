from .exceptions import DatabaseWriteDenied
from django.conf import settings
from django.http import HttpResponse
from django.utils.encoding import iri_to_uri


class HttpResponseReload(HttpResponse):
    """
    Reload page and stay on the same page from where request was made.
    """
    status_code = 302
    
    def __init__(self, request):
        HttpResponse.__init__(self)
        referer = request.META.get('HTTP_REFERER')
        self['Location'] = iri_to_uri(referer or "/")


class DatabaseReadOnlyMiddleware(object):
    def process_exception(self, request, exception):
        # Only process DatabaseWriteDenied exceptions
        if not isinstance(exception, DatabaseWriteDenied):
            return None
        
        # Handle the exception
        if request.method == 'POST':
            if getattr(settings, 'DB_READ_ONLY_MIDDLEWARE_MESSAGE', False):
                from django.contrib import messages
                messages.error(request, 'The site is currently in read-only '
                    'mode. Please try editing later.')
            
            # Try to redirect to this page's GET version
            return HttpResponseReload(request)
        else:
            # We can't do anything about this error
            return HttpResponse('The site is currently in read-only mode. '
                'Please try again later.')
