from __future__ import unicode_literals
from django.conf.urls import patterns, url

from apps.httplog.views import RequestsView


urlpatterns = patterns('',
    url(r'^$', RequestsView.as_view(), name='requests'),
)
