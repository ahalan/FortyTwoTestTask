from django.conf.urls import patterns, url

from apps.profile.views import ProfileHomeView, ProfileEditView


urlpatterns = patterns(
    '',
    url(r'^$', ProfileHomeView.as_view(), name='home'),
    url(r'^edit/(?P<profile_id>\d+)/$',
        ProfileEditView.as_view(), name='edit'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
)
