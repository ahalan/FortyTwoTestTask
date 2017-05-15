from __future__ import unicode_literals

from django.conf import settings
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
                latlng = GeoIP(
                    path=settings.GEOIP_PATH,
                    city=settings.GEOIP_CITY,
                    country=settings.GEOIP_COUNTRY
                ).coords(client_ip)
            except Exception as e:
                print "Error: %s" % e
                latlng = None

            request.user.lng, request.user.lat = latlng or (None, None)

        return None
