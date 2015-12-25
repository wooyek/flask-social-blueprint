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
PRODUCTION = not os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
DEBUG = not PRODUCTION

if not PRODUCTION:
    # there is no point in reconfiguring logging in production for gae
    # even development server with multi-process architecture is hard to grasp
    # in development server there are multiple root loggers
    # that are hard to reconfigure from here
    import website.logcfg
    website.logcfg.setup_logging()

SRC_DIR = os.path.abspath(os.path.dirname(__file__))

# Collect all zip packages paths then add them do sys.path
LIB_DIR = os.path.join(SRC_DIR, 'lib')
if os.path.exists(LIB_DIR):
    for path in os.listdir(LIB_DIR):
        path = os.path.join(LIB_DIR, path)
        if path.endswith(".zip") and path not in sys.path:
            logging.debug("Appending %s to sys.path" % path)
            sys.path.append(path)
    if LIB_DIR not in sys.path:
        logging.debug("Appending %s to path", LIB_DIR)
        sys.path.append(LIB_DIR)

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

if not PRODUCTION:
    # enable jinja debugging info in GAE SDK
    # http://jinja.pocoo.org/docs/faq/#my-tracebacks-look-weird-what-s-happening
    from google.appengine.tools.devappserver2.python import sandbox
    sandbox._WHITE_LIST_C_MODULES += ['_ctypes', 'gestalt', 'pwd']

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

    if not PRODUCTION:
        # werkzeug logs tracebacks to the environ['wsgi.errors']
        # which is set to dummy StringIO by the GAE development server
        # this will ensure traceback are shown in the console

        @app.before_request
        def setup_wsgi_errors():
            from flask import request
            request.environ['wsgi.errors'] = sys.stderr
