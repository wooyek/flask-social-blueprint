# coding=utf-8
# Created 2014 by Janusz Skonieczny
import logging
import os
import sys

# Setup simple logging fast, load a more complete logging setup later on
# Log a message each time this module get loaded.
logging.basicConfig(format='%(asctime)s %(levelname)-7s %(module)s.%(funcName)s - %(message)s')
logging.getLogger().setLevel(logging.DEBUG)
logging.disable(logging.NOTSET)
logging.info('Loading %s, app version = %s', __name__, os.getenv('CURRENT_VERSION_ID'))


# Detect if running on development server or in production environment
# The simplest auto detection is to detect if appliaction is run from here
# production environment would use WSGI app
PRODUCTION = __name__ != "__main__"
DEBUG = not PRODUCTION

SRC_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_FOLDER = os.path.join(SRC_DIR, "templates")
STATIC_FOLDER = os.path.join(SRC_DIR, "static")
STATIC_URL = '/static/'

try:
    import flask_social_blueprint
except ImportError:
    # in case we run it from the repo, put that repo on path
    import sys
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(SRC_DIR)), "src"))

from flask import Flask

app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER, static_url_path=STATIC_URL)
app.debug = DEBUG
app.testing = DEBUG  # WARNING: this will disable login_manager decorators


# -------------------------------------------------------------
# Load settings from separate modules
# -------------------------------------------------------------

import website.settings
app.config.from_object(website.settings)

config = "website.settings.production" if PRODUCTION else "website.settings.local"
import importlib
try:
    cfg = importlib.import_module(config)
    logging.debug("Loaded %s" % config)
    app.config.from_object(cfg)
except ImportError:
    logging.warning("Local settings module not found: %s", config)


# -------------------------------------------------------------
# Custom add ons
# -------------------------------------------------------------

from website.database import db
db.init_app(app)

# Enable i18n and l10n
from flask_babel import Babel
babel = Babel(app)

import auth.models
auth.models.init_app(app)

import auth.views
app.register_blueprint(auth.views.app)


# -------------------------------------------------------------
# Development server setup
# -------------------------------------------------------------

if app.debug:
    from werkzeug.debug import DebuggedApplication
    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

if __name__ == "__main__":
    # for convenience in setting up OAuth ids and secretes we use the example.com domain.
    # This should allow you to circumvent limits put on localhost/127.0.0.1 usage
    # Just map dev.example.com on 127.0.0.1 ip address.
    logging.debug("PRODUCTION: %s" % PRODUCTION)
    logging.debug("app.debug: %s" % app.debug)
    logging.debug("app.testing: %s" % app.testing)

    # making your the server externally visible simplifies networking configuration
    # for local vagrant based development
    logging.warn("We're binding to all your ip addresses. Don't forget to map `dev.example.com` to one of them")
    logging.warn("For more information see http://bit.ly/1xKtf8j")
    app.run(host="0.0.0.0", port=5055)
