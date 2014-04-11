# coding=utf-8
# Copyright 2014 Janusz Skonieczny

import os
from setuptools import setup, find_packages
from pip.req import parse_requirements

install_requires = parse_requirements(os.path.join(os.path.dirname(__file__), "requirements.txt"))

setup_kwargs = {
    'name': "flask-social-blueprint",
    'version': "0.6",
    'packages': find_packages("src"),
    'package_dir': {'': 'src'},
    'install_requires': [str(r.req) for r in install_requires],

    # metadata for upload to PyPI
    'author': "Janusz Skonieczny",
    # 'author_email': "",
    'description': "An OAuth based authentication blueprint for flask. Easy to extend and override",
    'license': "MIT",
    'keywords': "flask social oauth authentication",
    'url': "https://github.com/wooyek/flask-social-blueprint",
}

setup(**setup_kwargs)

