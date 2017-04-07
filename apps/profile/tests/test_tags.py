from __future__ import unicode_literals

from django.template import Context, Template
from django.test import TestCase

from apps.profile.models import Profile


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
