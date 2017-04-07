from __future__ import unicode_literals

import sys

from django.test import TestCase
from django.core import management
from StringIO import StringIO


class CommandTest(TestCase):
    """ Test for core commands """

    def test_get_model_list_command(self):
        """ Test for core command """

        out = StringIO()
        saved_stderr = sys.stderr

        try:
            sys.stderr = out
            management.call_command('get_models_list')
            self.assertIn('error:', out.getvalue())
        finally:
            sys.stderr = saved_stderr
