from __future__ import unicode_literals

import datetime
import operator

try:
    from django.conf import settings
    from django.utils import timezone
    has_timezone = True
except ImportError:
    has_timezone = False

from wtforms import fields, widgets
from wtforms.compat import string_types
from wtforms.validators import ValidationError

__all__ = (
    'ModelSelectField', 'QuerySetSelectField', 'DateTimeField'
)


class QuerySetSelectField(fields.SelectFieldBase):
    """A :class:`~wtforms.fields.SelectField` with the choices
    populated from the results of a Django
    :class:`~django.db.models.query.QuerySet`.

    .. code-block:: python

        category = QuerySetSelectField(queryset=Category.objects.all())

    The values passed in the request are the primary keys, but the
    ``data`` attribute of the field will be the actual model instance.

    By default each option displays the result of ``str(instance)``, but
    this can be customized by passing the ``get_label`` argument.

    To customize the query based on the request, you can set the
    ``queryset`` attribute after creating the form instance. For
    example, to limit the values based on the logged in user:

    .. code-block:: python

        class ArticleEdit(Form):
            title = StringField()
            series = QuerySetSelectField(allow_blank=True)

        def edit_article(request, id):
            article = Article.objects.get(pk=id)
            form = ArticleEdit(obj=article)
            form.series.queryset = Series.objects.filter(author=request.user)
            ...

    :param queryset: Populate the select with results from this query.
    :param get_label: The name of a model attribute to use to get the
        label for each item. Or a callable that takes a model instance
        and returns a label for it.
    :param allow_blank: Add a blank choice to the top of the list.
        Selecting it sets ``data`` to ``None``.
    :param blank_text: The label for the blank choice.
    """

    widget = widgets.Select()

    def __init__(self, label=None, validators=None, queryset=None, get_label=None, allow_blank=False, blank_text='', **kwargs):
        super(QuerySetSelectField, self).__init__(label, validators, **kwargs)
        self.allow_blank = allow_blank
        self.blank_text = blank_text
        self._set_data(None)
        if queryset is not None:
            self.queryset = queryset.all()  # Make sure the queryset is fresh

        if get_label is None:
            self.get_label = lambda x: x
        elif isinstance(get_label, string_types):
            self.get_label = operator.attrgetter(get_label)
        else:
            self.get_label = get_label

    def _get_data(self):
        if self._formdata is not None:
            for obj in self.queryset:
                if obj.pk == self._formdata:
                    self._set_data(obj)
                    break
        return self._data

    def _set_data(self, data):
        self._data = data
        self._formdata = None

    data = property(_get_data, _set_data)

    def iter_choices(self):
        if self.allow_blank:
            yield ('__None', self.blank_text, self.data is None)

        for obj in self.queryset:
            yield (obj.pk, self.get_label(obj), obj == self.data)

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == '__None':
                self.data = None
            else:
                self._data = None
                self._formdata = int(valuelist[0])

    def pre_validate(self, form):
        if not self.allow_blank or self.data is not None:
            for obj in self.queryset:
                if self.data == obj:
                    break
            else:
                raise ValidationError(self.gettext('Not a valid choice'))


class ModelSelectField(QuerySetSelectField):
    """Like a :class:`QuerySetSelectField`, except takes a model class
    to query all of its objects instead of a specific query.

    .. code-block:: python

        category = ModelSelectField(model=Category)

    :param: model: The model to query.
    """

    def __init__(self, label=None, validators=None, model=None, **kwargs):
        super(ModelSelectField, self).__init__(label, validators, queryset=model._default_manager.all(), **kwargs)


class DateTimeField(fields.DateTimeField):
    """A :class:`~wtforms.fields.DateTimeField` with support for
    Django's timezone utilities.
    """

    def __init__(self, *args, **kwargs):
        if not has_timezone:
            raise ImportError('DateTimeField does not work without Django >= 1.5')
        super(DateTimeField, self).__init__(*args, **kwargs)

    def process_formdata(self, valuelist):
        super(DateTimeField, self).process_formdata(valuelist)
        date = self.data
        if settings.USE_TZ and date is not None and timezone.is_naive(date):
            current_timezone = timezone.get_current_timezone()
            self.data = timezone.make_aware(date, current_timezone)

    def _value(self):
        date = self.data
        if settings.USE_TZ and isinstance(date, datetime.datetime) and timezone.is_aware(date):
            self.data = timezone.localtime(date)
        return super(DateTimeField, self)._value()
