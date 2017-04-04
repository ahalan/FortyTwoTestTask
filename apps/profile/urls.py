from django.conf.urls import patterns, url

from apps.profile.views import ProfileHomeView, ProfileEditView


urlpatterns = patterns(
    '',
    url(r'^$', ProfileHomeView.as_view(), name='home'),
    url(r'^edit/$', ProfileEditView.as_view(), name='edit'),
)
