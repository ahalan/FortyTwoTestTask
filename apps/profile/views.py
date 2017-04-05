from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.base import View

from apps.profile.models import Profile


class HomeView(View):
    """ Class based view for home page """

    template_name = "about.html"

    def get(self, request):
        profile = Profile.objects.first()
        return render(request, self.template_name, {'profile': profile})
