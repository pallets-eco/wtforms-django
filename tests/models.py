from __future__ import unicode_literals

from django.db import models

try:
    from localflavor.us.models import USStateField
except ImportError:
    from django.contrib.localflavor.us.models import USStateField


class Group(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return "%s(%d)" % (self.name, self.pk)

    __str__ = __unicode__


class User(models.Model):
    username = models.CharField(max_length=40)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL)
    birthday = models.DateField(help_text="Teh Birthday")
    email = models.EmailField(blank=True)
    posts = models.PositiveSmallIntegerField()
    state = USStateField()
    reg_ip = models.IPAddressField("IP Addy")
    url = models.URLField()
    file = models.FilePathField()
    file2 = models.FileField(upload_to=".")
    bool = models.BooleanField()
    time1 = models.TimeField()
    slug = models.SlugField()
    nullbool = models.NullBooleanField()
