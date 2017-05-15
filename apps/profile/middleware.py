from __future__ import unicode_literals

import os

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
                g = GeoIP(path=settings.GEOIP_PATH)
                print settings.GEOIP_PATH, os.path.isdir(settings.GEOIP_PATH)
                print "City: ", settings.GEOIP_CITY, g._city, g._city_file,\
                    os.path.isfile(g._city_file)
                print "Country: ", settings.GEOIP_COUNTRY, g._country,\
                    g._country_file, os.path.isfile(g._country_file)

                latlng = g.coords(client_ip)
            except Exception as e:
                print "Error: %s" % e
                latlng = None

            request.user.lng, request.user.lat = latlng or (None, None)

        return None
