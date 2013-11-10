WTForms-Django
==============

.. module:: wtforms_django

This extension provides templatetags to make it easier to work with Django
templates and WTForms' html attribute rendering. It also provides a generator
for automatically creating forms based on Django ORM models.

Templatetags
------------
.. module:: wtforms_django.templatetags.wtforms

Django templates does not allow arbitrarily calling functions with parameters,
making it impossible to use the html attribute rendering feature of WTForms. To
alleviate this, we provide a templatetag.

Adding :mod:`wtforms_django` to your INSTALLED_APPS will make the wtforms 
template library available to your application.  With this you can pass extra 
attributes to form fields similar to the usage in jinja:

.. code-block:: django

    {% load wtforms %}

    {% form_field form.username class="big_text" onclick="do_something()" %}

**Note** By default, using the ``{{ form.field }}`` syntax in django models will
be auto-escaped.  To avoid this happening, use Django's ``{% autoescape off %}``
block tag or use WTForms' `form_field` template tag.

Model forms
-----------
.. module:: wtforms_django.orm

.. autofunction:: model_form(model, base_class=Form, only=None, exclude=None, field_args=None, converter=None)

    :func:`model_form` attempts to glean as much metadata as possible from
    inspecting the model's fields, and will even attempt to guess at what
    validation might be wanted based on the field type. For example, converting
    an `EmailField` will result in a :class:`~wtforms.fields.StringField` with
    the :class:`~wtforms.validators.Email` validator on it. if the `blank`
    property is set on a model field, the resulting form field will have the
    :class:`~wtforms.validators.Optional` validator set.

    Just like any other Form, forms created by model_form can be extended via
    inheritance::

        UserFormBase = model_form(User)

        class UserForm(UserFormBase):
            new_pass     = PasswordField('', [validators.optional(), validators.equal_to('confirm_pass')])
            confirm_pass = PasswordField()

    When combined with :meth:`form iteration <wtforms.form.Form.__iter__>`,
    model_form is a handy way to generate dynamic CRUD forms which update with
    added fields to the model. One must be careful though, as it's possible the
    generated form fields won't be as strict with validation as a hand-written
    form might be.

ORM-backed fields
-----------------
.. module:: wtforms_django.fields


While linking data to most fields is fairly easy, making drop-down select lists
using django ORM data can be quite repetitive. To this end, we have added some
helpful tools to use the django ORM along with wtforms.


.. autoclass:: QuerySetSelectField(default field args, queryset=None, get_label=None, allow_blank=False, blank_text=u'')

    .. code-block:: python

        class ArticleEdit(Form):
            title    = StringField()
            column   = QuerySetSelectField(get_label='title', allow_blank=True)
            category = QuerySetSelectField(queryset=Category.objects.all())

        def edit_article(request, id):
            article = Article.objects.get(pk=id)
            form = ArticleEdit(obj=article)
            form.column.queryset = Column.objects.filter(author=request.user)

    As shown in the above example, the queryset can be set dynamically in the
    view if needed instead of at form construction time, allowing the select
    field to consist of choices only relevant to the user.

.. autoclass:: ModelSelectField(default field args, model=None, get_label='', allow_blank=False, blank_text=u'')

.. autoclass:: DateTimeField