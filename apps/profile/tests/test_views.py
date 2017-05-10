from __future__ import unicode_literals

import json

from django.conf import settings
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from apps.profile.models import Profile
from apps.profile.forms import ProfileEditForm


class AuthViewsTests(TestCase):
    """ Tests for auth views """

    def setUp(self):
        self.client = Client()

    def test_login_page_valid(self):
        """ Tests for auth with valid data """

        data = {
            'username': 'ahalan',
            'password': '12345'
        }
        response = self.client.post(
            reverse('profile:login'), data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated())
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)

    def test_login_page_invalid(self):
        """ Tests for auth with invalid data """

        data = {
            'username': 'test',
            'password': 'test'
        }
        response = self.client.post(
            reverse('profile:login'), data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated())
        self.assertEqual(
            response.context['form'].errors,
            {u'__all__': [u'Please enter a correct username and '
                          u'password. Note that both fields may '
                          u'be case-sensitive.']}
        )


class ProfileHomeViewsTest(TestCase):
    """ Tests for profile views """

    def setUp(self):
        self.client = Client()
        self.home_path = reverse('profile:home')

    def test_home_page_with_auth(self):
        """ Test homepage view for authorized user with profile """

        self.client.login(username='ahalan', password='12345')
        response = self.client.get(self.home_path)
        profile = auth.get_user(self.client).profile

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

    def test_home_page_without_auth(self):
        """ Test homepage view for non-authorized user """

        response = self.client.get(self.home_path)
        profile = Profile.objects.first()

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


class ProfileEditViewsTest(TestCase):
    """ Tests for profile edit views """

    def setUp(self):
        self.client = Client()
        self.edit_path = reverse('profile:edit')

    def test_get_edit_page_with_auth(self):
        """ Test profile edit view with authorized user """

        self.client.login(username='ahalan', password='12345')
        response = self.client.get(self.edit_path, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit.html')
        self.assertTrue('<!DOCTYPE html>' in response.content)
        self.assertTrue('form' in response.context.keys())
        self.assertEqual(response.context['form'].__class__, ProfileEditForm)

    def test_get_edit_page_without_auth(self):
        """ Test profile edit view without authorized user """

        response = self.client.get(self.edit_path, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            "{0}?next={1}".format(settings.LOGIN_URL, self.edit_path)
        )

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
        self.client.login(username='ahalan', password='12345')
        response = self.client.post(
            self.edit_path, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(content, {"payload": {}, "success": True})

    def test_post_edit_page_invalid(self):
        """ Test profile edit view on post request with invalid data"""

        data = {
            'first_name': 'test',
            'last_name': '',
            'biography': '',
            'email': 'INVALID',
            'skype': 'test',
            'jabber': 'INVALID',
            'other_contacts': '',
            'birthday': 'INVALID'
        }
        self.client.login(username='ahalan', password='12345')
        response = self.client.post(
            self.edit_path, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
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
        self.assertIn('last_name', content['payload']['errors'])
        self.assertEqual(
            content['payload']['errors']['last_name'],
            [u'This field is required.']
        )
