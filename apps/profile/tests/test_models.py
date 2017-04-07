from __future__ import unicode_literals

from django.test import TestCase

from apps.profile.models import Profile


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
