from django.conf import settings

import readonly.context_processors


def test_context_processor():
    request = {}
    context = readonly.context_processors.readonly(request)
    assert "SITE_READ_ONLY" in context
    assert context["SITE_READ_ONLY"] == settings.SITE_READ_ONLY

