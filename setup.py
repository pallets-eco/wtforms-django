#! /usr/bin/python
import io
from setuptools import find_packages, setup

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="WTForms-Django",
    version="0.2dev",
    url="https://github.com/wtforms/wtforms-django",
    project_urls={
        "Documentation": "https://wtforms-django.readthedocs.io/",
        "Code": "https://github.com/wtforms/wtforms",
        "Issue tracker": "https://github.com/wtforms/wtforms/issues",
    },
    license="BSD",
    maintainer="WTForms team",
    maintainer_email="davidism+wtforms@gmail.com",
    description="Integrates Django with WTForms.",
    long_description=readme,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=["WTForms>=2.1", "Django>=1.11"],
)
