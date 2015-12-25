# coding=utf-8
# Created 2014 by Janusz Skonieczny 


from datetime import datetime
import logging
import sqlalchemy as sa
from sqlalchemy import orm

from flask import current_app
from flask_babel import gettext as _
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, Security, SQLAlchemyUserDatastore

from website.database import db


# Setup Flask-Security
# http://pythonhosted.org/Flask-Security/quickstart.html#id1

roles_users = db.Table('roles_users',
                       sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id')),
                       sa.Column('role_id', sa.Integer(), sa.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(80), unique=True)
    description = sa.Column(sa.String(255))


class User(db.Model, UserMixin):
    id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.String(250), unique=True)
    email = sa.Column(sa.String(250), unique=True)
    password = sa.Column(sa.String(255))
    active = sa.Column(sa.Boolean)
    confirmed_at = sa.Column(sa.DateTime)
    created = sa.Column(sa.DateTime, default=datetime.now)
    is_staff = sa.Column(sa.Boolean)
    first_name = sa.Column(sa.String(120))
    last_name = sa.Column(sa.String(120))
    roles = orm.relationship('Role', secondary=roles_users, backref=orm.backref('users', lazy='dynamic'))

    @property
    def cn(self):
        if not self.first_name or not self.last_name:
            return self.email
        return u"{} {}".format(self.first_name, self.last_name)

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

    def social_connections(self):
        return SocialConnection.query.filter(SocialConnection.user_id == self.id).all()

# Setup Flask-Social
# http://pythonhosted.org/Flask-Social/#configuration

class SocialConnection(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    user = orm.relationship("User", foreign_keys=user_id, backref=orm.backref('connections', order_by=id))
    provider = sa.Column(sa.String(255))
    profile_id = sa.Column(sa.String(255))
    username = sa.Column(sa.String(255))
    email = sa.Column(sa.String(255))
    access_token = sa.Column(sa.String(255))
    secret = sa.Column(sa.String(255))
    first_name = sa.Column(sa.String(255))
    last_name = sa.Column(sa.String(255))
    cn = sa.Column(sa.String(255))
    profile_url = sa.Column(sa.String(512))
    image_url = sa.Column(sa.String(512))

    def get_user(self):
        return self.user

    @classmethod
    def by_profile(cls, profile):
        provider = profile.data["provider"]
        return cls.query.filter(cls.provider == provider, cls.profile_id == profile.id).first()

    @classmethod
    def from_profile(cls, user, profile):
        if not user or user.is_anonymous:
            email = profile.data.get("email")
            if not email:
                msg = "Cannot create new user, authentication provider did not not provide email"
                logging.warning(msg)
                raise Exception(_(msg))
            conflict = User.query.filter(User.email == email).first()
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
            db.session.add(user)
            db.session.flush()

        assert user.id, "User does not have an id"
        connection = cls(user_id=user.id, **profile.data)
        db.session.add(connection)
        db.session.commit()
        return connection


def load_user(user_id):
    return User.query.get(user_id)


def send_mail(msg):
    logging.debug("msg: %s" % msg)
    mail = current_app.extensions.get('mail')
    mail.send(msg)


def init_app(app):

	# Flask-Login
	# https://flask-login.readthedocs.org/en/latest/
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(load_user)
    login_manager.login_view = "/login"

    # Setup Flask-Security
    security = Security()
    security = security.init_app(app, SQLAlchemyUserDatastore(db, User, Role))
    security.send_mail_task(send_mail)

    from flask_social_blueprint.core import SocialBlueprint
    SocialBlueprint.init_bp(app, SocialConnection, url_prefix="/_social")
