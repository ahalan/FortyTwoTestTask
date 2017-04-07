from __future__ import unicode_literals

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
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

    def test_image_resize(self):
        """ Tests if submited image gets resized """

        profile = Profile.objects.first()
        profile.photo = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('assets/img/empty.jpg', 'rb').read(),
            content_type='image/jpeg')
        profile.save()

        self.assertEqual(settings.PHOTO_DIMENSIONS_HIGHT, profile.photo.height)
        self.assertEqual(settings.PHOTO_DIMENSIONS_WIDTH, profile.photo.width)
