from __future__ import unicode_literals

from django import forms
from django.forms.widgets import TextInput, Textarea

from apps.profile.models import Profile
from apps.profile.widgets import CalendarWidget


class ProfileEditForm(forms.ModelForm):
    """
    Edit profile form
    """

    class Meta:
        model = Profile
        fields = (
            'first_name', 'last_name', 'birthday','biography',
            'email', 'jabber', 'skype', 'other_contacts', 'photo'
        )
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'birthday': CalendarWidget(),
            'biography': Textarea(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'jabber': TextInput(attrs={'class': 'form-control'}),
            'skype': TextInput(attrs={'class': 'form-control'}),
            'other_contacts': Textarea(attrs={'class': 'form-control'}),
        }
