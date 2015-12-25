# coding=utf-8
# Created 2014 by Janusz Skonieczny
import logging
import os
import tempfile
import unittest
import flask_social_blueprint

from main import app
from website import database


class TestFlaskSocialBlueprint(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_file = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + self.db_file
        self.app = app.test_client()
        with app.app_context():
            database.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_file)

    def test_root_requires_login(self):
        # simple smoke test
        rv = self.app.get('/')
        logging.debug("rv: %s" % rv.headers)
        self.assertEqual(302, rv.status_code)
        assert rv.headers.get('Location').startswith("http://localhost/login")

    def test_not_redirect_loop(self):
        # simple smoke test
        rv = self.app.get('/login')
        logging.debug("rv: %s" % rv.headers)
        self.assertEqual(200, rv.status_code)
