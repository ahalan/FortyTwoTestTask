from __future__ import unicode_literals

from django.contrib.gis.geoip import GeoIP
from ipware.ip import get_ip


class GeolocationMiddleware(object):
    """ Setting coordinates from request ip for authorized user """

    def process_request(self, request):
        if request.user.is_authenticated():
            client_ip = get_ip(request)

            try:
                latlng = GeoIP().coords(client_ip)
            except Exception:
                latlng = None

            request.user.lng, request.user.lat = latlng or (None, None)

        return None
