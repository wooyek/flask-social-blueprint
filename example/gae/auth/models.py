# coding=utf-8
# Created 2014 by Janusz Skonieczny 

from datetime import datetime
import logging
from google.appengine.ext import ndb
from google.appengine.ext.ndb.model import BooleanProperty, StringProperty, DateTimeProperty, KeyProperty, IntegerProperty

from flask import current_app
from flask_babel import gettext as _, ngettext as __
from flask_security import UserMixin, RoleMixin

# Setup Flask-Security
# http://pythonhosted.org/Flask-Security/quickstart.html#id1

__all__ = ('Role', 'User', 'SocialConnection')


class Role(RoleMixin, ndb.Model):
    name = StringProperty()
    description = StringProperty(indexed=False)


class User(UserMixin, ndb.Model):
    email = StringProperty(required=True)
    password = StringProperty(indexed=False)
    active = BooleanProperty(indexed=False)
    confirmed_at = DateTimeProperty(indexed=False)
    created = DateTimeProperty(indexed=False, auto_now_add=True)
    is_staff = BooleanProperty(indexed=False, default=False)
    first_name = StringProperty(indexed=False)
    last_name = StringProperty(indexed=False)
    roles = KeyProperty(repeated=True, kind=Role)

    @property
    def cn(self):
        if not self.first_name or not self.last_name:
            return self.email
        return u"{} {}".format(self.first_name, self.last_name)

    @property
    def id(self):
        return self.key.urlsafe()

    @classmethod
    def by_email(cls, email):
        return cls.query().filter(cls.email == email).get()

    @property
    def gravatar(self):
        email = self.email.strip()
        if isinstance(email, unicode):
            email = email.encode("utf-8")
        import hashlib
        encoded = hashlib.md5(email).hexdigest()
        return "https://secure.gravatar.com/avatar/%s.png" % encoded

    def social_connection(self, provider):
        return SocialConnection.query(ancestor=self.key).filter(SocialConnection.provider == provider).get()

    def social_connections(self):
        return SocialConnection.query(ancestor=self.key).fetch(10)


# Setup Flask-Social
# http://pythonhosted.org/Flask-Social/#configuration

class SocialConnection(ndb.Model):
    provider = StringProperty()
    profile_id = StringProperty()
    username = StringProperty(indexed=False)
    email = StringProperty(indexed=False)
    access_token = StringProperty(indexed=False)
    secret = StringProperty(indexed=False)
    first_name = StringProperty(indexed=False)
    last_name = StringProperty(indexed=False)
    cn = StringProperty()  # common name, full name
    profile_url = StringProperty(indexed=False)
    image_url = StringProperty(indexed=False)

    def get_user(self):
        return self.key.parent().get()


    @classmethod
    def by_profile(cls, profile):
        provider = profile.data["provider"]
        return cls.query().filter(cls.provider == provider, cls.profile_id == profile.id).get()

    @classmethod
    def from_profile(cls, user, profile):
        if not user or user.is_anonymous:
            email = profile.data.get("email")
            if not email:
                msg = "Cannot create new user, authentication provider did not not provide email"
                logging.warning(msg)
                raise Exception(_(msg))
            conflict = User.query(User.email == email).get()
            if conflict:
                msg = "Cannot create new user, email {} is already used. Login and then connect external profile."
                msg = _(msg).format(email)
                logging.warning(msg)
                raise Exception(msg)

            now = datetime.now()
            user = User(
                email=email,
                first_name=profile.data.get("first_name"),
                last_name=profile.data.get("last_name"),
                confirmed_at=now,
                active=True,
            )

        def tx():
            if not user.key or not user.key.id():
                # we can call allocate ids beforehand but it will result in datastore call anyway
                # it will be simpler if we just put model here
                user.put()
            connection = cls(parent=user.key, **profile.data)
            connection.put()
            return connection

        return ndb.transaction(tx)


from google.appengine.ext import ndb
from flask_security import Security
from flask_security.datastore import Datastore, UserDatastore


class AppEngineDatastore(Datastore):
    def put(self, model):
        model.put()
        return model

    def commit(self):
        pass

    def delete(self, model):
        model.key.delete()

    def _build_query(self, model, parent=None, **kwargs):
        logging.debug("kwargs: %s" % kwargs)
        q = model.query(ancestor=parent)
        for name, value in kwargs.items():
            name = getattr(model, name)
            q = q.filter(name == value)
        return q


class AppEngineUserDatastore(AppEngineDatastore, UserDatastore):
    """A SQLAlchemy datastore implementation for Flask-Security that assumes the
    use of the Flask-SQLAlchemy extension.
    """
    def __init__(self, user_model, role_model):
        UserDatastore.__init__(self, user_model, role_model)

    def get_user(self, id_or_email):
        logging.debug("id_or_email: %s" % id_or_email)
        returned = None
        if self._is_numeric(id_or_email):
            returned = self.user_model.query.get(id_or_email)
        if not returned:
            returned = self.user_model.query().filter(self.user_model.email == id_or_email).get()
        return returned

    def _is_numeric(self, value):
        try:
            int(value)
        except ValueError:
            return False
        return True

    def find_user(self, **kwargs):
        if "id" in kwargs:
            return ndb.Key(urlsafe=kwargs.pop("id")).get()

        q = self._build_query(self.user_model, **kwargs)
        return q.get()

    def find_role(self, role):
        q = self._build_query(self.user_model, name=role)
        return q.get()


class AppEngineConnectionDatastore(AppEngineDatastore):
    """A SQLAlchemy datastore implementation for Flask-Social."""

    def __init__(self, connection_model):
        self.connection_model = connection_model

    def find_connection(self, **kwargs):
        return self.find_connections(**kwargs).get()

    def find_connections(self, **kwargs):
        logging.debug("kwargs: %s" % kwargs)
        parent = ndb.Key(urlsafe=kwargs.pop("user_id")) if "user_id" in kwargs else None
        provider = kwargs.pop("provider_id")
        return self._build_query(self.connection_model, parent=parent, provider=provider)

    def create_connection(self, **kwargs):
        parent = ndb.Key(urlsafe=kwargs.pop("user_id")) if "user_id" in kwargs else None
        provider = kwargs.pop("provider_id")
        if provider != 'google':
            connection = self.connection_model(parent=parent, provider=provider, **kwargs)
        else:
            dn = kwargs.pop("display_name")
            fn = kwargs.pop("full_name")
            dn = "{givenName} {familyName}".format(**dn)
            fn = "{givenName} {familyName}".format(**fn)
            connection = self.connection_model(parent=parent, provider=provider, display_name=dn, full_name=fn, **kwargs)
        return connection.put()


def load_user(user_id):
    return ndb.Key(urlsafe=user_id).get()


def send_mail(msg):
    logging.debug("msg: %s" % msg)
    from google.appengine.api import mail
    email = mail.EmailMessage()
    email.body = msg.body
    email.html = msg.html
    email.sender = msg.sender
    email.to = msg.recipients
    email.send()


def init_app(app):
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(load_user)
    login_manager.login_view = "/login"

    # Setup Flask-Security
    security = Security()
    security = security.init_app(app, AppEngineUserDatastore(User, Role))
    security.send_mail_task(send_mail)

    from flask_social_blueprint.core import SocialBlueprint
    SocialBlueprint.init_bp(app, SocialConnection, url_prefix="/_social")
