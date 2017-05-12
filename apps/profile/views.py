from __future__ import unicode_literals

import json

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.http import HttpResponse

from apps.profile.models import Profile
from apps.profile.forms import ProfileEditForm


def get_user_profile(user):
    """ Returns user profile if exists else returns first profile """

    if not hasattr(user, 'profile'):
        profile = Profile.objects.first()
    else:
        profile = user.profile
    return profile


class ProfileHomeView(TemplateView):
    """ Class based view for home page """

    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileHomeView, self).get_context_data(**kwargs)
        context['profile'] = get_user_profile(self.request.user)
        return context


class ProfileEditView(UpdateView):
    """ Class based view editing profile """

    template_name = "edit.html"
    form_class = ProfileEditForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileEditView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return get_user_profile(self.request.user)

    def form_valid(self, form):
        if self.request.is_ajax():
            context = {
                'success': True,
                'payload': {}
            }
            self.object = form.save()

            if self.object.photo:
                context['payload']['photo_url'] = self.object.photo.url
            return self.render_to_json_response(context)

        return super(ProfileEditView, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            context = {
                'success': False,
                'payload': {
                    'errors': dict(form.errors.items())
                }
            }
            return self.render_to_json_response(context)

        return super(ProfileEditView, self).form_valid(form)

    def render_to_json_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(json.dumps(context), **response_kwargs)


class MessengerView(TemplateView):
    """ Class based view for messenger page """

    template_name = "messenger.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MessengerView, self).dispatch(*args, **kwargs)
