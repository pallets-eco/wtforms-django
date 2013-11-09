import sys
import os
TESTS_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

##########################################################################
# -- Django Initialization
#
# Unfortunately, we cannot do this in the setUp for a test case, as the
# settings.configure method cannot be called more than once, and we cannot
# control the order in which tests are run, so making a throwaway test won't
# work either.

from django.conf import settings
settings.configure(
    INSTALLED_APPS=['tests', 'wtforms_django'],
    # Django 1.0 to 1.3
    DATABASE_ENGINE='sqlite3',
    TEST_DATABASE_NAME=':memory:',

    # Django 1.4+
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    }
)

from django.db import connection
connection.creation.create_test_db(verbosity=0)

CONFIGURED = True
