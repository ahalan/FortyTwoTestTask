from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from apps.profile.models import Profile


class HomeView(View):
    """ Class based view for home page """

    template_name = "profile/about.html"

    def get(self, request):
        profile = get_object_or_404(Profile, id=1)
        return render(request, self.template_name, {'profile': profile})
