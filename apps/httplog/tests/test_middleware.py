from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from apps.httplog.models import HttpRequestEntry


class HttpLogerMiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.path = reverse('httplog:requests')

    def test_httprequest_logger(self):
        """ Test http request middleware """

        self.client.get(self.path)
        entry = HttpRequestEntry.objects.get(path=self.path)

        self.assertEqual(HttpRequestEntry.objects.count(), 1)
        self.assertEquals(entry.method, 'GET')
        self.assertEquals(entry.path, self.path)
