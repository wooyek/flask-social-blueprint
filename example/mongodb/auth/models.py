# -*- coding: utf-8 -*-

import logging

from datetime import datetime

from mongoengine import Q, fields, QuerySet
from mongoengine import NULLIFY, CASCADE, DENY, PULL
from mongoengine import OperationError, ValidationError, NotUniqueError
from mongoengine.signals import post_save, post_delete
from flask_mongoengine import MongoEngine

from flask_security import Security, MongoEngineUserDatastore, url_for_security
from flask_security import login_required, roles_required, roles_accepted
from flask_security import current_user
from flask_security.utils import encrypt_password
from flask_security import UserMixin, RoleMixin, AnonymousUser

from flask_babel import gettext as _

db = MongoEngine()
security = Security()

Document = db.Document
EmbeddedDocument = db.EmbeddedDocument
DynamicDocument = db.DynamicDocument
queryset_manager = db.queryset_manager

class Role(Document, RoleMixin):
    name = db.StringField(required=True, unique=True, max_length=80)
    description = db.StringField(max_length=255)
    
    def __unicode__(self):
        return self.name

    meta = {
        'collection': 'role',
        'indexes': ['name'],
    }

"""
 curl -u a83a9f143473601d5118793a33a5a4dc29c5b70f:x-oauth-basic https://api.github.com/user
{
  "login": "srault95",
  "id": 1041983,
  "avatar_url": "https://avatars.githubusercontent.com/u/1041983?v=3",
  "gravatar_id": "",
  "url": "https://api.github.com/users/srault95",
  "html_url": "https://github.com/srault95",
  "followers_url": "https://api.github.com/users/srault95/followers",
  "following_url": "https://api.github.com/users/srault95/following{/other_user}",
  "gists_url": "https://api.github.com/users/srault95/gists{/gist_id}",
  "starred_url": "https://api.github.com/users/srault95/starred{/owner}{/repo}",
  "subscriptions_url": "https://api.github.com/users/srault95/subscriptions",
  "organizations_url": "https://api.github.com/users/srault95/orgs",
  "repos_url": "https://api.github.com/users/srault95/repos",
  "events_url": "https://api.github.com/users/srault95/events{/privacy}",
  "received_events_url": "https://api.github.com/users/srault95/received_events",
  "type": "User",
  "site_admin": false,
  "name": "StÃ©phane RAULT",
  "company": null,
  "blog": "http://www.radical-spam.org",
  "location": "Paris",
  "email": null,
  "hireable": false,
  "bio": null,
  "public_repos": 12,
  "public_gists": 0,
  "followers": 0,
  "following": 3,
  "created_at": "2011-09-11T07:23:52Z",
  "updated_at": "2014-12-18T12:36:56Z",
  "private_gists": 0,
  "total_private_repos": 5,
  "owned_private_repos": 5,
  "disk_usage": 228,
  "collaborators": 0,
  "plan": {
    "name": "small",
    "space": 1228800,
    "collaborators": 0,
    "private_repos": 10
  }
}

        emails = json.loads(r.text or r.content)

        name_split = profile.get('name', "").split(" ", 1)
        data = {
            "provider": "Github",
            "profile_id": str(profile["id"]),
            "username": profile.get('login'),
            "email": emails[0].get("email"),
            "access_token": access_token,
            "secret": None,
            "first_name": name_split[0],
            "last_name": name_split[1] if len(name_split) > 1 else None,
            "cn": profile.get('name'),
            "profile_url": profile["html_url"],
            "image_url": profile["avatar_url"],
        }
        return ExternalProfile(str(profile['id']), data, raw_data)


"""    

class User(Document, UserMixin):

    email = db.StringField(unique=True, max_length=255)
    
    password = db.StringField(max_length=120)
    
    active = db.BooleanField(default=True)
    
    remember_token = db.StringField(max_length=255)
    
    authentication_token = db.StringField(max_length=255)

    roles = fields.ListField(fields.ReferenceField(Role, reverse_delete_rule=DENY), default=[])

    first_name = db.StringField(max_length=120)

    last_name = db.StringField(max_length=120)

    confirmed_at = fields.DateTimeField()
    
    created = fields.DateTimeField(default=datetime.utcnow())
    
    @property
    def cn(self):
        if not self.first_name or not self.last_name:
            return self.email
        return u"{} {}".format(self.first_name, self.last_name)

    @classmethod
    def by_email(cls, email):
        return cls.objects(email=email).first()

    @property
    def gravatar(self):
        email = self.email.strip()
        if isinstance(email, unicode):
            email = email.encode("utf-8")
        import hashlib
        encoded = hashlib.md5(email).hexdigest()
        return "https://secure.gravatar.com/avatar/%s.png" % encoded

    def social_connections(self):
        return SocialConnection.objects(user=self)

    def set_password(self, password, save=False):
        u""" Méthode pour faciliter affectation de password sans charger à chaque fois :
        flask.ext.security.utils.encrypt_password
        """
        self.password = encrypt_password(password)
        if save:
            self.save()
    
    def __unicode__(self):
        return self.email

    meta = {
        'collection': 'user',
        'indexes': ['email', 'roles'],
    }

class SocialConnection(Document):
    """
'secret': None, 'image_url': u'https://avatars.githubusercontent.com/u/1041983?v=3', 
'provider': 'Github', 'email': u'stephane.rault@radicalspam.org', 'profile_url': u'https://github.com/srault95'}
    
    """
    user = fields.ReferenceField(User)
    
    # Github|Twitter|Facebook|Google
    provider = db.StringField(max_length=255)
    profile_id = db.StringField(max_length=255)

    #'username': u'xxxx'
    username = db.StringField(max_length=255)
    email = db.StringField(max_length=255)
    access_token = db.StringField(max_length=255)
    
    #Not use ?
    secret = db.StringField(max_length=255)
    
    first_name = db.StringField(max_length=255, help_text=_(u"First Name"))
    last_name = db.StringField(max_length=255, help_text=_(u"Last Name"))
    
    cn = db.StringField(max_length=255, help_text=_(u"Common Name"))
    
    profile_url = db.StringField(max_length=512)
    image_url = db.StringField(max_length=512)
    
    def get_user(self):
        return self.user

    @classmethod
    def by_profile(cls, profile):
        provider = profile.data["provider"]
        return cls.objects(provider=provider, profile_id=profile.id).first()

    @classmethod
    def from_profile(cls, user, profile):
        if not user or user.is_anonymous():
            email = profile.data.get("email")
            if not email:
                msg = "Cannot create new user, authentication provider did not not provide email"
                logging.warning(msg)
                raise Exception(_(msg))
            conflict = User.objects(email=email).first()
            if conflict:
                msg = _("Cannot create new user, email {} is already used. Login and then connect external profile.").format(email)
                logging.warning(msg)
                raise Exception(msg)

            now = datetime.now()
            user = User(
                #login=profile.data.get('login'),
                email=email,
                first_name=profile.data.get("first_name"),
                last_name=profile.data.get("last_name"),
                confirmed_at=now,
                active=True,
            ).save()

        print "profile.data : ", profile.data
        """
        {'username': u'srault95', 'last_name': u'RAULT', 'cn': u'St\xe9phane RAULT', 'profile_id': '1041983', 'first_name': u'St\xe9phane', 'access_token': u'70ed4a47f7042b2ad2048e57d78b3e350db2604b', 'secret': None, 'image_url': u'https://avatars.githubusercontent.com/u/1041983?v=3', 'provider': 'Github', 'email': u'stephane.rault@radicalspam.org', 'profile_url': u'https://github.com/srault95'}
        
        """
        connection = cls(user=user, **profile.data).save()
        #connection = cls(user_id=user.id, **profile.data).save()
        return connection


    def __unicode__(self):
        return self.display_name

    meta = {
        'collection': 'socialconnection',
        #'indexes': ['user_id'],
        'indexes': ['user', 'profile_id'],
    }

def send_mail(msg):
    logging.debug("msg: %s" % msg)
    mail = current_app.extensions.get('mail', None)
    if mail:
        mail.send(msg)

def init_app(app):
    
    from flask import flash, redirect, request

    datastore = MongoEngineUserDatastore(db, User, Role)
    security.init_app(app, datastore)
    
    @app.errorhandler(401)
    def unauthorized(error):
        flash(_(u"Please authenticate for see this page"), "error")
        return redirect(url_for_security('login', next=request.url))
    
    #security.send_mail_task(send_mail)

    from flask_social_blueprint.core import SocialBlueprint
    SocialBlueprint.init_bp(app, SocialConnection, url_prefix="/_social")
    
    @app.before_first_request
    def before_first_request():
        for m in [User, Role, SocialConnection]:
            m.drop_collection()
