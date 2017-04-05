from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Profile(User):
    """
    Model represents user's profile
    """

    birthday = models.DateField(
        verbose_name=_("Date of birth"),
        blank=True, null=True
    )
    biography = models.TextField(
        verbose_name=_('Biography'),
        null=True, blank=True
    )
    jabber = models.EmailField(
        verbose_name=_('Jabber'),
        null=True, blank=True
    )
    skype = models.CharField(
        verbose_name=_('Skype'),
        max_length=23,
        null=True, blank=True
    )
    other_contacts = models.TextField(
        verbose_name=_('Other contacts'),
        null=True, blank=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __unicode__(self):
        return "{0} {1}".format(self.first_name, self.last_name)
