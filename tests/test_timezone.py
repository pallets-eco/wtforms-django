from __future__ import unicode_literals, absolute_import

from . import django_setup
assert django_setup.CONFIGURED

import datetime
import django

from django.test import TestCase as DjangoTestCase
from wtforms import Form
from wtforms_django.fields import DateTimeField
from .utils import DummyPostData


if django.VERSION >= (1, 5):
    from django.utils import timezone
    from django.test.utils import override_settings
    has_timezone = True
else:
    def override_settings(*args, **kw):
        def decorator(func):
            return func
        return decorator

    has_timezone = False


class DateTimeFieldTimezoneTest(DjangoTestCase):

    class F(Form):
        a = DateTimeField()

    @override_settings(USE_TZ=True, TIME_ZONE='America/Los_Angeles')
    def test_convert_input_to_current_timezone(self):
        if not has_timezone:
            return
        post_data = {'a': ['2013-09-24 00:00:00']}
        form = self.F(DummyPostData(post_data))
        self.assertTrue(form.validate())
        date = form.data['a']
        assert date.tzinfo
        self.assertEquals(
            timezone._get_timezone_name(date.tzinfo),
            timezone._get_timezone_name(timezone.get_current_timezone()))

    @override_settings(USE_TZ=True, TIME_ZONE='America/Los_Angeles')
    def test_stored_value_converted_to_current_timezone(self):
        if not has_timezone:
            return

        utc_date = datetime.datetime(2013, 9, 25, 2, 15, tzinfo=timezone.utc)
        form = self.F(a=utc_date)
        self.assertTrue('2013-09-24 19:15:00' in form.a())
