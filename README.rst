WTForms-Django
==============

WTForms-Django is a fork of the ``wtforms.ext.django`` package from WTForms.
The package has been renamed to ``wtforms_django`` but otherwise should
function the same as ``wtforms.ext.django`` did.

to install::
	
	pip install WTForms-Django


Rationale
---------

The reasoning for splitting out this package is that WTForms 2.0 has
deprecated all its ``wtforms.ext.<library>`` packages and they will
not receive any further feature updates. The authors feel that packages
for companion libraries work better with their own release schedule and
the ability to diverge more from WTForms.

This package is currently looking for a maintainer. If you want to help
maintain this package please contact davidism@gmail.com.
