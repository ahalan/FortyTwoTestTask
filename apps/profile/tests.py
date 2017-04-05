from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from apps.profile.models import Profile


class ViewsTest(TestCase):
    """ Tests for profile views """

    def setUp(self):
        self.client = Client()

    def test_homepage(self):
        """ Test homepage view when profile exists """

        profile = Profile.objects.first()
        response = self.client.get(reverse('profile:home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
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


class ModelTest(TestCase):
    """ Tests for profile models """

    def test_profile_creation(self):
        """ Test profile instance creation """
        count_before = Profile.objects.count()
        Profile.objects.create(**{
            "first_name": "Andrey",
            "last_name": "Halan",
            "email": "halan.andrey@gmail.com",
            "username": "newuser"
        })
        self.assertEquals(Profile.objects.count(), count_before + 1)
