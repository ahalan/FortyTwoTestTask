#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "fortytwo_test_task.settings")

    from django.core.management import execute_from_command_line
    from django.core.management import call_command

    call_command("flush")

    execute_from_command_line(sys.argv)
