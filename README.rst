flask-social-blueprint
======================

An OAuth based authentication blueprint for flask. Easy to extend and
override.

https://github.com/wooyek/flask-social-blueprint

.. image:: https://travis-ci.org/wooyek/flask-social-blueprint.svg

.. image:: https://coveralls.io/repos/wooyek/flask-social-blueprint/badge.svg?branch=develop&service=github 
    :target: https://coveralls.io/github/wooyek/flask-social-blueprint?branch=develop

.. image:: https://img.shields.io/pypi/v/flask-social-blueprint.svg?maxAge=2592000   
    :target: https://pypi.python.org/pypi/flask-social-blueprint/   

.. image:: https://img.shields.io/pypi/dm/flask-social-blueprint.svg?maxAge=2592000   
    :target: https://pypi.python.org/pypi/flask-social-blueprint/

Demo
----

Based on ``example/gae`` codebase with secret ``settings_prd.py``
provided for proper OAuth providers configuration.

http://flask-social-blueprint.appspot.com/

Why?
----

There is `Flask-Social`_ extension, but is painfully interconnected and
to change anything you basically have to fork and rewrite portions of
it.

Not to mention that it requires POST request on social login endpoints.
I hate that I need to write an inline forms to create a login button.

How it’s any better?
--------------------

This blueprint plays nicely with `Flask-Security`_ and it’s easily
overridable without forking everything, it’s `plain simple OOP`_ not that
`module based provider`_ `function search crap`_.

To extend it just write a provider class anywhere you want, and setup
it’s client id and secret in the flask settings providing an import path
like this:

.. code:: python

    SOCIAL_BLUEPRINT = {
        # https://developers.facebook.com/apps/
        "flask_social_blueprint.providers.Facebook": {
            # App ID
            'consumer_key': '197…',
            # App Secret
            'consumer_secret': 'c956c1…'
        },
        # https://apps.twitter.com/app/new
        "flask_social_blueprint.providers.Twitter": {
            # Your access token from API Keys tab
            'consumer_key': 'bkp…',
            # access token secret
            'consumer_secret': 'pHUx…'
        },
        # https://console.developers.google.com/project
        "flask_social_blueprint.providers.Google": {
            # Client ID
            'consumer_key': '797….apps.googleusercontent.com',
            # Client secret
            'consumer_secret': 'bDG…'
        },
        # https://github.com/settings/applications/new
        "flask_social_blueprint.providers.Github": {
            # Client ID
            'consumer_key': '6f6…',
            # Client Secret
            'consumer_secret': '1a9…'
        },
    }

Done!

What’s missing?
---------------

This is just authentication blueprint there is no templates, models and
stuff that you would want to customize yourself.

What to do more?
----------------

1. More providers
2. Make Flask-Security dependency optional

Examples
--------

The core of this module has no GUI, but examples have a nice login
and profile page to show it it works. Checkout the `demo`_.

.. image:: https://github.com/wooyek/flask-social-blueprint/raw/master/docs/login-form.png
   :alt: Flask social blueprint login form example
   :align: center


.. image:: https://github.com/wooyek/flask-social-blueprint/raw/master/docs/user-profile.png
   :alt: Flask social blueprint user profile example
   :align: center

The example has a working model and templates, has a bunch of
dependencies like `Flask-SLQAlchemy`_, you can take it as a wire frame
modify and build your app with that.

Examples are made from some existing apps, they may contain more stuff
that’s really needed to showcase this module. When in trouble just ask
questions.

Or just drop in this solution inside your working Flask app. It should
not create any conflicts with existing stuff. You maybe required to
write an adapter for your User model and SocialConnection model (or
similar) but that’s 3 functions for the adapter. All User model
requirements come from `Flask-security`_.

1. for `SQLAlchemy <example/sqla/README.md>`_
2. for `Google App Engine <example/gae/README.md>`_
3. for `MongoDB <example/mongodb/README.md>`_


Development environment with Vagrant
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can always use our `vagrant`_. It should set up everything needed for tests or
development. This should set up everything you need:

.. code:: sh

    vagrant up --provision

The code will be kept in ``/vagrant/`` directory.
You have will get 3 python virtual enviroments setup:

* gae – for gae example
* sqla – for sqla example
* mongodb – for mongodb example

Activate one of them using `virtualenvwrapper`_. For example to activate mongodb:

.. code:: sh

    workon mongodb
    python /vagrant/example/mongodb/main.py

Google App Engine example have to be run little bit different, 
it needs GAE development server layer wrapping Flask.

.. code:: sh

    workon gae
    python ~/google_appengine/dev_appserver.py --host 0.0.0.0 --port 5055 /vagrant/example/gae/

When you develope with and without vagrant because please remeber that `flask-social-blueprint/example/gae/lib/`
will be shared between machines, it may cause problems.

Setup OAuth with different providers
------------------------------------

This blueprint needs client id's and secrets provided by social services you
want to integrate with, here's where you setup them.

In examples we use http://dev.example.com:5055 URL to overcome limitations
posed on `localhost` and `127.0.0.1` when setting up integrations.
The http://example.com URL is guaranteed to be valid and may be used by
anyone in demos and documentation. Just map `dev.example.com` to `127.0.0.1`
and you're good to go.

Callback URLs use the name of the provider at the end.
Obtain client ids and secrets from OAuth providers using
main URL http://dev.example.com:5055 and callbacks URLS like these:

- http://dev.example.com:5055/_social/callback/Google
- http://dev.example.com:5055/_social/callback/Facebook
- http://dev.example.com:5055/_social/callback/Twitter
- http://dev.example.com:5055/_social/callback/Github

Twitter
^^^^^^^

Create new application here: https://apps.twitter.com/app/new

Google
^^^^^^

1. Create new project here: https://console.developers.google.com/project
2. In APIs & auth > Credentials create Client ID
3. Update consent screen details, at least product name, home page and email address
4. Enable Google+ API

GitHub
^^^^^^

Create new application here: https://github.com/settings/applications/new

Facebook
^^^^^^^^

Create new application here: https://developers.facebook.com/apps/

Setup `Valid OAuth redirect URIs` in Settings > Advanced > Security


.. _Flask-Social: https://pythonhosted.org/Flask-Social/
.. _Flask-Security: https://pythonhosted.org/Flask-Security/
.. _Flask-SLQAlchemy: https://pythonhosted.org/Flask-SQLAlchemy/
.. _demo: http://flask-social-blueprint.appspot.com/
.. _plain simple OOP: src/flask_social_blueprint/providers.py
.. _module based provider: https://github.com/mattupstate/flask-social/blob/develop/flask_social/core.py#L127
.. _function search crap: https://github.com/mattupstate/flask-social/tree/develop/flask_social/providers
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/
.. _vagrant: https://www.vagrantup.com/
