from __future__ import unicode_literals

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.middleware import AuthenticationMiddleware

from apps.profile.middleware import GeolocationMiddleware


class GeolocationMiddlewareTest(TestCase):
    """ Tests for geolocation middleware """

    def setUp(self):
        self.locations = {
            '213.109.233.142': [24.709699630737305, 48.92150115966797],
            '127.0.0.1': ['', '']
        }
        self.rf = RequestFactory()
        self.middleware = GeolocationMiddleware()
        self.request = self.rf.get(reverse('profile:home'))
        self.request.session = {}

        # adds user instance to request
        AuthenticationMiddleware().process_request(self.request)

    def test_geolocation_middleware_with_auth(self):
        """ Test geolocation middleware with auth """
        self.request.user.is_authenticated = lambda: True

        for ip, latlng in self.locations.items():
            self.request.META['REMOTE_ADDR'] = ip
            self.assertIsNone(self.middleware.process_request(self.request))
            self.assertTrue(hasattr(self.request.user, 'lat'))
            self.assertTrue(hasattr(self.request.user, 'lng'))
            self.assertEqual(self.request.user.lng, latlng[0])
            self.assertEqual(self.request.user.lat, latlng[1])

    def test_geolocation_middleware_without_auth(self):
        """ Test geolocation middleware without auth """

        self.assertIsNone(self.middleware.process_request(self.request))
        self.assertFalse(hasattr(self.request.user, 'lat'))
        self.assertFalse(hasattr(self.request.user, 'lng'))
