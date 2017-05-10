from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from apps.httplog.models import HttpRequestEntry


class HttpRequestsViewsTest(TestCase):
    """ Tests for httplog views """

    def setUp(self):
        self.client = Client()

        HttpRequestEntry.objects.bulk_create([
            HttpRequestEntry(
                method='GET',
                host='localhost',
                path='/',
                status_code=200
            ) for i in range(20)
        ])

    def test_requests_page(self):
        """ Test requests page view """

        response = self.client.get(reverse('httplog:requests'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'requests.html')
        self.assertTrue('<!DOCTYPE html>' in response.content)

    def test_get_requests_history_is_ajax(self):
        """ Test requests history view with ajax request"""

        response = self.client.get(
            reverse('httplog:requests-history'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'block/requests_list.html')
        self.assertTrue('entries' in response.context)
        self.assertTrue('non_viewed_count' in response.context)

    def test_get_requests_history_is_not_ajax(self):
        """ Test requests history view by not ajax request"""

        response = self.client.get(reverse('httplog:requests-history'))
        self.assertEqual(response.status_code, 400)

    def test_get_requests_history_entry_on_page(self):
        """ Test requests history view on elements on page """

        last_ten_entries = HttpRequestEntry.objects.all()[
                           :settings.HTTP_LOG_ENTRIES_ON_PAGE]
        entry = last_ten_entries[0]

        response = self.client.get(
            reverse('httplog:requests-history'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertTrue(entry.method in response.content)
        self.assertTrue(entry.host in response.content)
        self.assertTrue(entry.path in response.content)

        self.assertEqual(
            len(response.context['entries']),
            settings.HTTP_LOG_ENTRIES_ON_PAGE
        )
        self.assertEqual(
            list(response.context['entries']),
            list(last_ten_entries))

    def test_post_requests_history_priority_order(self):
        """ Test priority order after update entries """

        entries = HttpRequestEntry.objects.all()[
                  :settings.HTTP_LOG_ENTRIES_ON_PAGE]

        for i, item in enumerate(entries):
            item.priority = i + 1
            item.save()

        response = self.client.get(
            reverse('httplog:requests-history'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        entries = list(response.context['entries'])

        self.assertEqual(entries[0].priority, 10)
        self.assertEqual(entries[-1].priority, 1)

    def test_post_requests_history_valid(self):
        """ Test requests history view on update entries priority """

        entry = HttpRequestEntry.objects.first()
        payload = {'entry_id': entry.id, 'priority': 2}
        response = self.client.post(
            reverse('httplog:requests-history'), payload
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Success')

        entry = HttpRequestEntry.objects.get(id=payload['entry_id'])
        self.assertEqual(entry.priority, payload['priority'])

    def test_post_requests_history_invalid(self):
        """ Test requests history view with missing entries argument """

        response = self.client.post(reverse('httplog:requests-history'), {})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content, 'Missing argument `entry_id` or `priority`'
        )
