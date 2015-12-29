# coding=utf-8
# Copyright 2013 Janusz Skonieczny
from importlib import import_module
import logging

from flask_oauth import OAuthRemoteApp
from flask_babel import gettext as _

DEFAULT_PROPERTIES = ("user_id", "display_name", "first_name", "last_name", "email", "image_url")


class BaseProvider(OAuthRemoteApp):
    def __init__(self, *args, **kwargs):

        super(BaseProvider, self).__init__(None, *args, **kwargs)

    def get_profile(self, raw_data):
        raise NotImplementedError()


class ExternalProfile(object):
    def __init__(self, profile_id, data, raw_data):
        self.id = profile_id
        self.data = data
        self.raw_data = raw_data


class Twitter(BaseProvider):
    def __init__(self, *args, **kwargs):
        defaults = {
            'name': 'Twitter',
            'base_url': 'http://api.twitter.com/1/',
            'request_token_url': 'https://api.twitter.com/oauth/request_token',
            'access_token_url': 'https://api.twitter.com/oauth/access_token',
            'authorize_url': 'https://api.twitter.com/oauth/authenticate'
        }
        defaults.update(kwargs)
        super(Twitter, self).__init__(*args, **defaults)
        self.tokengetter(lambda: None)

    def get_profile(self, raw_data):
        logging.debug("data: %s" % raw_data)
        import twitter

        api = twitter.Api(consumer_key=self.consumer_key,
                          consumer_secret=self.consumer_secret,
                          access_token_key=raw_data['oauth_token'],
                          access_token_secret=raw_data['oauth_token_secret'],
                          cache=None)
        profile = api.VerifyCredentials()
        name_split = profile.name.split(" ", 1)
        data = {
            'provider': self.name,
            'profile_id': str(profile.id),
            'username': profile.screen_name,
            "email": None,  # twitter does not provide email
            'access_token': raw_data['oauth_token'],
            'secret': raw_data['oauth_token_secret'],
            "first_name": name_split[0],
            "last_name": name_split[1] if len(name_split) > 1 else None,
            'cn': profile.name,
            'profile_url': "http://twitter.com/{}".format(profile.screen_name),
            'image_url': profile.profile_image_url
        }
        return ExternalProfile(str(profile.id), data, raw_data)


class Google(BaseProvider):
    def __init__(self, *args, **kwargs):
        defaults = {
            'name': 'Google',
            'base_url': 'https://www.google.com/accounts/',
            'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
            'access_token_url': 'https://accounts.google.com/o/oauth2/token',
            'request_token_url': None,
            'access_token_method': 'POST',
            'access_token_params': {
                'grant_type': 'authorization_code'
            },
            'request_token_params': {
                'response_type': 'code',
                'scope': 'https://www.googleapis.com/auth/plus.me email'
            }
        }
        defaults.update(kwargs)
        super(Google, self).__init__(*args, **defaults)

    def get_profile(self, raw_data):
        access_token = raw_data['access_token']
        import oauth2client.client as googleoauth
        import apiclient.discovery as googleapi
        import httplib2

        credentials = googleoauth.AccessTokenCredentials(
            access_token=access_token,
            user_agent=''
        )
        http = httplib2.Http()
        http = credentials.authorize(http)
        api = googleapi.build('plus', 'v1', http=http)
        profile = api.people().get(userId='me').execute()
        name = profile.get('name')
        data = {
            'provider': "Google",
            'profile_id': profile['id'],
            'username': None,
            "email": profile.get('emails')[0]["value"],
            'access_token': access_token,
            'secret': None,
            "first_name": name.get("givenName"),
            "last_name": name.get("familyName"),
            'cn': profile.get('displayName'),
            'profile_url': profile.get('url'),
            'image_url': profile.get('image', {}).get("url")
        }
        return ExternalProfile(str(profile['id']), data, raw_data)


class Facebook(BaseProvider):
    def __init__(self, *args, **kwargs):
        defaults = {
            'name': 'Facebook',
            'base_url': 'https://graph.facebook.com/',
            'request_token_url': None,
            'access_token_url': '/oauth/access_token',
            'authorize_url': 'https://www.facebook.com/dialog/oauth',
            'request_token_params': {
                'scope': 'email'
            }
        }
        defaults.update(kwargs)
        super(Facebook, self).__init__(*args, **defaults)

    def get_profile(self, raw_data):
        access_token = raw_data['access_token']
        import facebook

        graph = facebook.GraphAPI(access_token)
        profile = graph.get_object("me", fields=["email", "first_name", "last_name", "name"])
        profile_id = profile['id']
        data = {
            "provider": "Facebook",
            "profile_id": profile_id,
            "username": profile.get('username'),
            "email": profile.get('email'),
            "access_token": access_token,
            "secret": None,
            "first_name": profile.get('first_name'),
            "last_name": profile.get('last_name'),
            "cn": profile.get('name'),
            "profile_url": "http://facebook.com/profile.php?id={}".format(profile_id),
            "image_url": "http://graph.facebook.com/{}/picture".format(profile_id),
        }
        return ExternalProfile(profile_id, data, raw_data)


class Github(BaseProvider):
    def __init__(self, *args, **kwargs):
        defaults = {
            'name': 'Github',
            'base_url': 'https://github.com/',
            'authorize_url': 'https://github.com/login/oauth/authorize',
            'access_token_url': 'https://github.com/login/oauth/access_token',
            'request_token_url': None,
            'request_token_params': {
                'response_type': 'code',
                'scope': 'user:email'
            }
        }
        defaults.update(kwargs)
        super(Github, self).__init__(*args, **defaults)

    def get_profile(self, raw_data):
        logging.debug("raw_data: %s" % raw_data)
        access_token = raw_data['access_token']

        import requests
        import json
        r = requests.get('https://api.github.com/user?access_token={}'.format(access_token))
        if not r.ok:
            raise Exception(_("Could not load profile data from Github API"))
        profile = json.loads(r.text or r.content)

        r = requests.get('https://api.github.com/user/emails?access_token={}'.format(access_token))
        if not r.ok:
            raise Exception(_("Could not load emails data from from Github API"))
        emails = json.loads(r.text or r.content)

        name = profile.get('name') or ""
        name_split = name.split(" ", 1)
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
