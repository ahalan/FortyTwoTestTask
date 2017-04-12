from __future__ import unicode_literals

from django.test import TestCase
from django.core import management
from django.db import models

from StringIO import StringIO


class CoreCommandTest(TestCase):
    """ Test for core commands """

    def setUp(self):
        self.models = models.get_models(include_auto_created=True)

    def test_get_model_list_command(self):
        """ Test output of get_model_list command """
        out, err = StringIO(), StringIO()
        management.call_command('get_models_list', stdout=out, stderr=err)

        for model in self.models:
            info = "model - {model}; count - {count}\n".format(
                model=model.__name__,
                count=model.objects.count())
            error = "error: {0}".format(info)
            self.assertIn(info, out.getvalue())
            self.assertIn(error, err.getvalue())
