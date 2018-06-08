import sys
import os

TESTS_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "../src"))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

##########################################################################
# -- Django Initialization
#
# Unfortunately, we cannot do this in the setUp for a test case, as the
# settings.configure method cannot be called more than once, and we cannot
# control the order in which tests are run, so making a throwaway test won't
# work either.

import django
from django.conf import settings
from . import django_settings


settings.configure(default_settings=django_settings)
django.setup()

from django.db import connection

connection.creation.create_test_db(verbosity=0)

CONFIGURED = True
