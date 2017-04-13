from __future__ import unicode_literals

from django.conf import settings


def on_page(request):
    """ Adds HTTP_LOG_ENTRIES_ON_PAGE to template context. """
    return {'on_page': settings.HTTP_LOG_ENTRIES_ON_PAGE}
