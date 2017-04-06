from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from apps.profile.models import Profile
from apps.profile.forms import ProfileEditForm


class ProfileHomeView(View):
    """ Class based view for home page """

    template_name = "profile.html"

    def get(self, request):
        profile = Profile.objects.first()
        return render(request, self.template_name, {'profile': profile})


class ProfileEditView(View):
    """ Class based view editing profile """

    template_name = "edit.html"
    form_class = ProfileEditForm

    def get(self, request):
        form = self.form_class(instance=Profile.objects.first())
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        response_data = dict(success=True, payload={})
        form = self.form_class(
            request.POST,
            request.FILES,
            instance=Profile.objects.first()
        )
        if form.is_valid():
            profile = form.save()
            if profile.photo:
                response_data['payload']['photo_url'] = profile.photo.url
        else:
            response_data['success'] = False
            response_data['payload']['errors'] = dict(form.errors.items())

        return HttpResponse(json.dumps(response_data),
                            content_type="application/json")

