from __future__ import unicode_literals

from django.test import TestCase

from apps.httplog.models import HttpRequestEntry


class HttpRequestEntryModelTest(TestCase):
    """ Tests for httplog models """

    def test_httplog_entry_creation(self):
        """ Test httplog instance creation """

        entry = HttpRequestEntry.objects.create(
            method='GET',
            host='localhost',
            path='/',
            status_code=200
        )
        self.assertEquals(HttpRequestEntry.objects.count(), 1)
        self.assertEquals(entry.priority, 1)
