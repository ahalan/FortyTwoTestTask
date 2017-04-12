from __future__ import unicode_literals

import json

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileEditView, self).dispatch(*args, **kwargs)

    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        form = self.form_class(instance=profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, profile_id):
        response_data = dict(success=True, payload={})
        profile = get_object_or_404(Profile, id=profile_id)
        form = self.form_class(
            request.POST,
            request.FILES,
            instance=profile
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
