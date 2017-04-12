from __future__ import unicode_literals

from django.test import TestCase
from django.test.client import Client

from apps.profile.forms import ProfileEditForm
from apps.profile.models import Profile


class ProfileFormsTest(TestCase):
    """ Tests for profile form """

    def setUp(self):
        self.client = Client()
        self.profile = Profile.objects.first()

    def test_edit_event_valid(self):
        """ Test profile form with valid data """

        data = {
            'first_name': 'test',
            'last_name': 'test',
            'biography': 'biography test',
        }
        form = ProfileEditForm(data, instance=self.profile)

        self.assertTrue(form.is_valid())

    def test_edit_event_invalid_field(self):
        """ Tests profile form with invalid data """

        data = {
            'jabber': 'INVALID'
        }
        form = ProfileEditForm(data, instance=self.profile)

        self.assertFalse(form.is_valid())
        self.assertIn('jabber', form.errors)
        self.assertEqual(
            form.errors['jabber'], [u'Enter a valid email address.'])

    def test_edit_event_required_field(self):
        """ Tests profile form for required fields """

        form = ProfileEditForm({}, instance=self.profile)

        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertEqual(
            form.errors['first_name'], [u'This field is required.'])
        self.assertEqual(
            form.errors['last_name'], [u'This field is required.'])
