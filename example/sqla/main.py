# coding=utf-8
# Created 2014 by Janusz Skonieczny
import logging
from flask import Flask
import os

# Setup simple logging fast, load a more complete logging setup later on
# Log a message each time this module get loaded.
logging.basicConfig(format='%(asctime)s %(levelname)-7s %(module)s.%(funcName)s - %(message)s')
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)
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
    sys.path.append(os.path.join(os.path.dirname(SRC_DIR), "../../src"))

app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER, static_url_path=STATIC_URL)
app.debug = DEBUG
app.testing = DEBUG  # WARNING: this will disable login_manager decorators

from website import settings
app.config.from_object(settings)

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
    # for coonvienience in setting up OAuth ids and secretes we use the example.com domain.
    # This should allow you to circumvent limits put on localhost/127.0.0.1 usage
    # Just map dev.example.com on 127.0.0.1 ip adress.
    logging.debug("PRODUCTION: %s" % PRODUCTION)
    logging.debug("app.debug: %s" % app.debug)
    logging.debug("app.testing: %s" % app.testing)
    logging.debug("Don't forget to map dev.example.com on 127.0.0.1 ip address")
    app.run("dev.example.com", 5055)
