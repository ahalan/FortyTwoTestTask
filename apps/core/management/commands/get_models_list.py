from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.db import models


class Command(BaseCommand):
    help = 'Prints all project models and the count of objects in every model'

    def handle(self, *args, **options):
        all_models = models.get_models(include_auto_created=True)

        for model in all_models:
            model_info = "model - {model}; count - {count}\n".format(
                model=model.__name__,
                count=model.objects.count()
            )

            self.stdout.write(model_info)
            self.stderr.write("error: {0}".format(model_info))
