from __future__ import unicode_literals

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from apps.core.models import CrudModelEntry


@receiver(post_save)
def post_save_signal(sender, created, **kwargs):
    """ Singal handle create/update actions for models """

    if sender.__name__ not in settings.EXCLUDE_FROM_MODELS_LOG:
        instance = kwargs.pop('instance', None)
        action = (CrudModelEntry.ACTION_CREATE if created
                  else CrudModelEntry.ACTION_UPDATE)

        CrudModelEntry.objects.create(
            action=action,
            model_name="{0}.{1}".format(
                sender._meta.app_label, sender.__name__),
            instance_id=instance.pk
        )


@receiver(post_delete)
def post_delete_signal(sender, **kwargs):
    """ Singal handle delete action for models """

    if sender.__name__ not in settings.EXCLUDE_FROM_MODELS_LOG:
        instance = kwargs.pop('instance', None)

        CrudModelEntry.objects.create(
            action=CrudModelEntry.ACTION_DELETE,
            model_name="{0}.{1}".format(
                sender._meta.app_label, sender.__name__),
            instance_id=instance.pk
        )
