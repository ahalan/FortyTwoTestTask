from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _


class ProfileEditForm(forms.Form):
    """
    Edit profile form
    """

    first_name = forms.CharField(label='Name', max_length=50)
    last_name = forms.CharField(label='Last name', max_length=50)
    birthday = forms.DateField(label='Date of birth')
    photo = forms.ImageField(required=False)
    biography = forms.CharField(label='Bio', widget=forms.Textarea, max_length=10000)
    email = forms.EmailField(label='Email')
    jabber = forms.EmailField(label='Jabber')
    skype = forms.CharField(label='Skype', max_length=50)
    other_contacts = forms.CharField(label='Other contacts',widget=forms.Textarea, max_length=10000)
