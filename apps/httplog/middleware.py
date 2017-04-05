from __future__ import unicode_literals

from models import HttpRequestEntry


class HttpRequestLoggerMiddleware(object):
    """
    Middleware that save http requests in the db
    """

    def process_response(self, request, response):
        HttpRequestEntry.objects.create(
            host=request.get_host(),
            path=request.path,
            method=request.method,
            status_code=response.status_code,
            user_agent=request.META.pop('HTTP_USER_AGENT', None),
        )
        return response