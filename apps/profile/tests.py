from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.test import TestCase
from django.test.client import Client

from apps.profile.models import Profile
from apps.profile.forms import ProfileEditForm


class ViewsTest(TestCase):
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

        Profile.objects.create(**PROFILE_DATA)
        response = self.client.get(reverse('profile:edit'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit.html')
        self.assertTrue('<!DOCTYPE html>' in response.content)

    def test_post_edit_page(self):
        """ Test profile edit view on post request """

        Profile.objects.create(**PROFILE_DATA)
        response = self.client.get(reverse('profile:edit'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit.html')
        self.assertTrue('<!DOCTYPE html>' in response.content)

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

        profile = Profile.objects.create(**PROFILE_DATA)
        profile.photo = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('assets/img/empty.jpg', 'rb').read(),
            content_type='image/jpeg')
        profile.save()

        self.assertEqual(settings.PHOTO_DIMENSIONS_HIGHT, profile.photo.height)
        self.assertEqual(settings.PHOTO_DIMENSIONS_WIDTH, profile.photo.width)


class FormsTest(TestCase):
    """ Tests for profile form """

    @classmethod
    def setUpClass(cls):
        management.call_command(
            'flush', interactive=False, load_initial_data=False
        )

    def setUp(self):
        self.profile = Profile.objects.create(**PROFILE_DATA)

    def test_edit_event(self):
        data = PROFILE_DATA
        data['first_name'] = 'test'
        data['biography'] = 'biography test'
        data['skype'] = 'skype test'
        data['jabber'] = 'jabber@test.com'

        form = ProfileEditForm(data, instance=self.profile)
        form.is_valid()
        self.assertTrue(form.is_valid())
