from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class HttpRequestEntry(models.Model):
    """
    Model represents http request history records
    """

    host = models.CharField(
        verbose_name=_("Hostname"),
        max_length=255
    )
    path = models.CharField(
        verbose_name=_("Path"),
        max_length=255
    )
    method = models.CharField(
        verbose_name=_("HTTP Method"),
        max_length=255
    )
    user_agent = models.CharField(
        verbose_name=_("User agent"),
        max_length=255,
        blank=True, null=True
    )
    time = models.DateTimeField(
        verbose_name=_("Request time"),
        auto_now_add=True
    )
    status_code = models.IntegerField(
        verbose_name=_("Status code")
    )
    viewed = models.BooleanField(
        verbose_name=_("Viewed"),
        default=False
    )
    priority = models.IntegerField(
        verbose_name=_("Priority"),
        default=0
    )

    class Meta:
        ordering = ['priority', '-time']
        verbose_name = _("Http Request Entry")
        verbose_name_plural = _("Http Request Entries")

    def __unicode__(self):
        return u"{time} | {method} | {host}{path}".format(
            time=self.time, method=self.method,
            host=self.host, path=self.path
        )
