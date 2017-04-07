from __future__ import unicode_literals

import json

from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.template import Context, Template

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


class FormsTest(TestCase):
    """ Tests for profile form """

    def setUp(self):
        self.client = Client()
        self.profile = Profile.objects.first()

    def test_edit_event_valid(self):
        """ Test profile form with valid data """

        data = {
            'first_name': 'test',
            'biography': 'biography test',
        }
        form = ProfileEditForm(data, instance=self.profile)

        self.assertTrue(form.is_valid())

    def test_edit_event_invalid(self):
        """ Tests profile form with invalid data """

        data = {
            'jabber': 'INVALID'
        }
        form = ProfileEditForm(data, instance=self.profile)

        self.assertFalse(form.is_valid())
        self.assertIn('jabber', form.errors)
        self.assertEqual(
            form.errors['jabber'], [u'Enter a valid email address.']
        )


class TemplateTagTest(TestCase):
    """ Tests for profile templatetag """

    def setUp(self):
        self.template = '{% load profile_tags %}{% edit_link obj %}'

    def render_template(self, template, context=None):
        context = context or {}
        context = Context(context)
        return Template(template).render(context)

    def test_edit_link_valid(self):
        """ Test edit_link tag with valid data """

        profile = Profile.objects.first()
        rendered = self.render_template(self.template, {'obj': profile})
        awaited_link = "/admin/{app}/{app}/{id}/".format(
            app=Profile._meta.app_label,
            id=profile.id
        )
        self.assertEqual(rendered, awaited_link)

    def test_edit_link_invalid(self):
        """ Test edit_link tag with invalid data """

        with self.assertRaises(ValueError):
            self.render_template(self.template, {'obj': 'INVALID'})
