from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from apps.httplog.models import HttpRequestEntry


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

    def test_requests_history_is_ajax(self):
        """ Test requests history view with ajax request"""

        response = self.client.get(
            reverse('httplog:requests-history'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'block/requests_list.html')

    def test_requests_history_is_not_ajax(self):
        """ Test requests history view by not ajax request"""

        response = self.client.get(reverse('httplog:requests-history'))
        self.assertEqual(response.status_code, 400)

    def test_requests_history_entry_on_page(self):
        """ Test requests history view on elements on page """

        HttpRequestEntry.objects.bulk_create([
            HttpRequestEntry(
                method='GET',
                host='localhost',
                path='/',
                status_code=200
            ) for i in range(20)
        ])
        response = self.client.get(
            reverse('httplog:requests-history'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(
            len(response.context['entries']),
            settings.HTTP_LOG_ENTRIES_ON_PAGE
        )


class ModelTest(TestCase):
    """ Tests for httplog models """

    def test_httplog_entry_creation(self):
        """ Test httplog instance creation """

        HttpRequestEntry.objects.create(
            method='GET',
            host='localhost',
            path='/',
            status_code=200
        )
        self.assertEquals(HttpRequestEntry.objects.count(), 1)


class MiddlewareTest(TestCase):
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
