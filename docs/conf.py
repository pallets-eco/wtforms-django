# -*- coding: utf-8 -*-
from __future__ import print_function

from pallets_sphinx_themes import ProjectLink, get_version

# Project --------------------------------------------------------------

project = "WTForms-Django"
copyright = "2008, WTForms team"
author = "WTForms team"
release, version = get_version("WTForms-Django")

# General --------------------------------------------------------------

master_doc = "index"

extensions = ["sphinx.ext.autodoc", "sphinx.ext.intersphinx"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "wtforms": ("https://wtforms.readthedocs.io/en/stable/", None),
    "django": (
        "https://docs.djangoproject.com/en/stable/",
        "https://docs.djangoproject.com/en/stable/_objects/",
    ),
}

# HTML -----------------------------------------------------------------

html_theme = "flask"
html_context = {
    "project_links": [
        ProjectLink("PyPI releases", "https://pypi.org/project/WTForms-Django/"),
        ProjectLink("Source Code", "https://github.com/wtforms/wtforms-django/"),
        ProjectLink("Issue Tracker", "https://github.com/wtforms/wtforms/issues/"),
    ]
}
html_sidebars = {
    "index": ["project.html", "searchbox.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html"],
}
html_show_sourcelink = False

# LaTeX ----------------------------------------------------------------

latex_documents = [
    (master_doc, project + ".tex", project + " Documentation", author, "manual")
]
