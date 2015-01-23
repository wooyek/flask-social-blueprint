# coding=utf-8
# Copyright 2014 Janusz Skonieczny
import sys
import os
import uuid
from setuptools import setup, find_packages
from pip.req import parse_requirements

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(ROOT_DIR, 'src')
sys.path.append(SRC_DIR)

install_requires = parse_requirements(
    os.path.join(os.path.dirname(__file__), "requirements.txt"),
    session=uuid.uuid1()
)
with open("README.rst") as readme:
    long_description = readme.read()

from flask_social_blueprint import __version__ as version

setup_kwargs = {
    'name': "flask-social-blueprint",
    'version': version,
    'packages': find_packages("src"),
    'package_dir': {'': 'src'},
    'install_requires': [str(r.req) for r in install_requires],

    # "package_data": {
    #     '': ['requirements.txt']
    # },

    'author': "Janusz Skonieczny",
    'author_email': "js@bravelabs.pl",
    'description': "An OAuth based authentication blueprint for flask. Easy to extend and override",
    'long_description': long_description,
    'license': "MIT",
    'keywords': "flask social oauth authentication",
    'url': "https://github.com/wooyek/flask-social-blueprint",
    'classifiers': [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    'test_suite': 'flask_social_blueprint.tests.suite'
}

setup(**setup_kwargs)

