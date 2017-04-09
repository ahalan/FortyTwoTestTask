from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class CrudModelEntry(models.Model):
    """
    Model represents db entry about the object creation/editing/deletion
    """

    ACTION_CREATE = 0
    ACTION_UPDATE = 1
    ACTION_DELETE = 2

    ACTION_CHOICES = (
        (ACTION_CREATE, 'Create'),
        (ACTION_UPDATE, 'Update'),
        (ACTION_DELETE, 'Delete')
    )

    action = models.CharField(
        verbose_name=_("Action"),
        choices=ACTION_CHOICES,
        max_length=2
    )
    model_name = models.CharField(
        verbose_name=_("Model name"),
        max_length=100
    )
    instance_id = models.IntegerField(
        verbose_name=_("Instance ID"),
    )
    timestamp = models.DateTimeField(
        verbose_name=_("Timestamp"),
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Model entry"
        verbose_name_plural = "Model entries"

    def __unicode__(self):
        return u'{0} {1} instance with id={2} at {3}'.format(
            self.action, self.model_name, self.instance_id, self.timestamp
        )
