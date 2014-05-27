flask-social-blueprint
======================

An OAuth based authentication blueprint for flask. Easy to extend and override.

## Why?

There is [Flask-Social](https://pythonhosted.org/Flask-Social/) extension,
but is painfully interconnected and to change anything you basically have
to fork and rewrite portions of it.

Not to mention that it requires POST request on social login endpoints.
I hate that I need to write an inline forms to create a login button.

## How it's any better?

This blueprint plays nicely with [Flask-Security](https://pythonhosted.org/Flask-Security/)
and it's easily overridable without forking everything, it's plain simple
OOP no that single module based provider search crap.

To extend it just write a provider class anywhere you want, and setup it's
client id and secret in the flask settings like this:

    "flask_social_blueprint.providers.Facebook": {
        'consumer_key': '197…',
        'consumer_secret': 'c956c1…'
    },

Done!

## What's missing?

This is just authentication blueprint there is no templates, models and stuff
that you would want to customize yourself.

The example has a working model and templates, has a bunch of dependencies like
Flask-SLQAlchemy, you can take it as a wire frame modify and build your app
with that.

Or just drop in this solution inside your working Flask app.
I should not create any conflicts with existing stuff. You maybe required to write
an adapter for your User model and SocialConnection model (or similar) but
that's 3 functions for the adapter. Any User model requirements come
from Flask_security.

## What to do more?

1. More providers
2. Make Flask-Security dependency optional


