from __future__ import unicode_literals

from django.conf import settings


def config(request):
    """
    Adds django settings to template context.
    """
    return {'settings': settings}
