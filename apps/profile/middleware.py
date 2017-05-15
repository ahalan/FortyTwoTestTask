from __future__ import unicode_literals

import os
from django.contrib.gis.geoip import GeoIP


class GeolocationMiddleware(object):
    """ Setting coordinates from request ip for authorized user """

    def process_request(self, request):
        if request.user.is_authenticated():
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

            if x_forwarded_for:
                client_ip = x_forwarded_for.split(',')[-1].strip()
            else:
                client_ip = request.META.get('REMOTE_ADDR')

            try:
                latlng = GeoIP().coords(client_ip)
            except Exception as e:
                print e
                print os.listdir("uploads/geoip")
                latlng = None

            request.user.lng, request.user.lat = latlng or (None, None)

        return None
