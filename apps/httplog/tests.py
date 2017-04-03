from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core import management
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client


class ViewsTest(TestCase):
    """ Tests for httplog views """

    def setUp(self):
        self.client = Client()

    def test_requests_page(self):
        """ Test requests page view """
        response = self.client.get(reverse('httplog:requests'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'requests.html')
        self.assertTrue('<!DOCTYPE html>' in response.content)

    def test_requests_page_is_ajax(self):
        """ Test requests page history view """
        response = self.client.get(
            reverse('httplog:requests-history'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'block/requests_list.html')

    def test_requests_page_is_not_ajax(self):
        """ Test requests page history view """
        response = self.client.get(reverse('httplog:requests-history'))
        self.assertEqual(response.status_code, 400)
