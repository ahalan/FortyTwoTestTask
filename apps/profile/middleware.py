from __future__ import unicode_literals

import os
import stat

from django.conf import settings
from django.contrib.gis.geoip import GeoIP


def change_permissions_recursive(path, mode):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in [os.path.join(root, d) for d in dirs]:
            os.chmod(dir, mode)
    for file in [os.path.join(root, f) for f in files]:
        os.chmod(file, mode)


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
                print "Error: %s" % e
                print "File: {}; Exists - {}; Permissions: {};".format(
                    settings.GEOIP_CITY,
                    os.path.isfile(settings.GEOIP_CITY),
                    oct(stat.S_IMODE(os.stat(settings.GEOIP_CITY).st_mode))
                )
                change_permissions_recursive(settings.MEDIA_ROOT, 0o777)
                latlng = None

            request.user.lng, request.user.lat = latlng or (None, None)

        return None
