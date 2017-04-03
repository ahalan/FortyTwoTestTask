from django.conf.urls import patterns, include, url
from django.contrib import admin

from apps.profile.views import AboutView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', AboutView.as_view(), name='home'),
)
