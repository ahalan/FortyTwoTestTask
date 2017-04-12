from __future__ import unicode_literals

import sys

from django.test import TestCase
from django.core import management
from django.db import models

from StringIO import StringIO


class CoreCommandTest(TestCase):
    """ Test for core commands """

    def setUp(self):
        self.models = models.get_models(include_auto_created=True)

    def test_get_model_list_command(self):
        """ Test for core command """

        out = StringIO()
        saved_stderr = sys.stderr
        sys.stderr = out

        management.call_command('get_models_list')

        for model in self.models:
            info = 'error: model - {model}; count - {count}\n'.format(
                model=model.__name__,
                count=model.objects.count())
            self.assertIn(info, out.getvalue())

        sys.stderr = saved_stderr
