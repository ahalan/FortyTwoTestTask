from __future__ import unicode_literals

import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from apps.profile.forms import ProfileEditForm
from apps.profile.models import Profile


class ProfileViewsTest(TestCase):
    """ Tests for profile views """

    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        """ Test homepage view when profile exists """

        profile = Profile.objects.first()
        response = self.client.get(reverse('profile:home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertTrue('<!DOCTYPE html>' in response.content)
        self.assertTrue('profile' in response.context.keys())
        self.assertEqual(profile, response.context['profile'])

        self.assertIn(profile.first_name, response.content)
        self.assertIn(profile.last_name, response.content)
        self.assertIn(profile.email, response.content)
        self.assertIn(profile.jabber, response.content)
        self.assertIn(profile.skype, response.content)
        self.assertIn(profile.biography, response.content)
        self.assertIn(profile.other_contacts, response.content)

    def test_get_edit_page(self):
        """ Test profile edit view on get request """

        response = self.client.get(reverse('profile:edit'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit.html')
        self.assertTrue('<!DOCTYPE html>' in response.content)
        self.assertTrue('form' in response.context.keys())
        self.assertEqual(response.context['form'].__class__, ProfileEditForm)

    def test_post_edit_page_valid(self):
        """ Test profile edit view on post request with valid data """

        data = {
            'first_name': 'test',
            'last_name': 'test',
            'biography': '',
            'email': 'test@test.com',
            'skype': 'test',
            'jabber': 'test@test.co',
            'other_contacts': '',
            'birthday': '2000-01-01'
        }
        response = self.client.post(reverse('profile:edit'), data)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(content, {"payload": {}, "success": True})

    def test_post_edit_page_invalid(self):
        """ Test profile edit view on post request with invalid data"""

        data = {
            'first_name': 'test',
            'last_name': 'test',
            'biography': '',
            'email': 'INVALID',
            'skype': 'test',
            'jabber': 'INVALID',
            'other_contacts': '',
            'birthday': 'INVALID'
        }
        response = self.client.post(reverse('profile:edit'), data)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        self.assertFalse(content['success'])
        self.assertIn('errors', content['payload'])

        self.assertIn('birthday', content['payload']['errors'])
        self.assertEqual(
            content['payload']['errors']['birthday'],
            [u'Enter a valid date.']
        )
        self.assertIn('jabber', content['payload']['errors'])
        self.assertEqual(
            content['payload']['errors']['jabber'],
            [u'Enter a valid email address.']
        )
        self.assertIn('email', content['payload']['errors'])
        self.assertEqual(
            content['payload']['errors']['email'],
            [u'Enter a valid email address.']
        )
