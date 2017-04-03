from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from profile.models import Profile

USER_DATA = {
    "id": 1,
    "first_name": "Andrey",
    "last_name": "Halan",
    "email": "halan.andrey@gmail.com",
    "username": "ahalan"
}

PROFILE_DATA = {
    "user_id": USER_DATA['id'],
    "birthday": "09-09-1993",
    "biography": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
            Phasellus vel diam quis libero dignissim ullamcorper.",

    "skype": "firestarter--",
    "jabber": "halan.andrey@42cc.co",
    "other_contacts": "ETC",
}


class ViewsTest(TestCase):
    """ Tests for profile views """

    def setUp(self):
        self.client = Client()

    def test_homepage(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
        self.assertTrue('<!DOCTYPE HTML>' in response.content)


class ModelTest(TestCase):
    """ Tests for profile models """

    def setUp(self):
        self.user = User.objects.create(**USER_DATA)


    def test_profile_creation(self):
        Profile.objects.create(**PROFILE_DATA)
        self.assertEquals(Profile.objects.count(), 1)
