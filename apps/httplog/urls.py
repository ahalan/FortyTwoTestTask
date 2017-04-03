from __future__ import unicode_literals
from django.conf.urls import patterns, url

from apps.httplog.views import RequestsHistoryPageView, RequestsHistoryView

urlpatterns = patterns(
    '',
    url(r'^$',
        RequestsHistoryPageView.as_view(),
        name='requests'),
    url(r'^get/history/$',
        RequestsHistoryView.as_view(),
        name='requests-history'),
)
