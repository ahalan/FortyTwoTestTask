from __future__ import unicode_literals

from django.test import TestCase
from django.db import IntegrityError

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

    def test_httplog_entry_creation_failed(self):
        """ Test httplog instance creation failed """
        with self.assertRaises(IntegrityError) as context:
            HttpRequestEntry.objects.create(
                method='GET',
                host='localhost',
                path='/',
            )

            error_msg = context.exception.message
            self.assertContains('status_code', error_msg)
            self.assertContains('NOT NULL constraint failed', error_msg)

    def test_httplog_entry_priority_order(self):
        """ Test httplog instance ordering """

        HttpRequestEntry.objects.bulk_create([
            HttpRequestEntry(
                method='GET',
                host='localhost',
                path='/',
                status_code=200
            ) for i in range(10)
        ])

        entry_before = HttpRequestEntry.objects.first()
        self.assertEquals(entry_before.priority, 1)

        entry_before.priority = 10
        entry_before.save()

        entry_after = HttpRequestEntry.objects.first()
        self.assertEquals(entry_after.priority, 10)
