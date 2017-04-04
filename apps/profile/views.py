from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from apps.profile.models import Profile
from apps.profile.forms import ProfileEditForm

class ProfileHomeView(View):
    """ Class based view for home page """

    template_name = "profile.html"

    def get(self, request):
        profile = get_object_or_404(Profile, id=1)
        return render(request, self.template_name, {'profile': profile})


class ProfileEditView(View):
    """ Class based view for home page """

    template_name = "edit.html"

    def get(self, request):
        return render(request, self.template_name, {'form': ProfileEditForm()})
