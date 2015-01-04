import os

SOCIAL_BLUEPRINT = {
    # https://developers.facebook.com/apps/
    "flask_social_blueprint.providers.Facebook": {
        # App ID
        'consumer_key': os.environ.get('FACEBOOK_KEY', ''),
        # App Secret
        'consumer_secret': os.environ.get('FACEBOOK_SECRET', '')
    },
    # https://apps.twitter.com/app/new
    "flask_social_blueprint.providers.Twitter": {
        # Your access token from API Keys tab
        'consumer_key': os.environ.get('TWITTER_KEY', ''),
        # access token secret
        'consumer_secret': os.environ.get('TWITTER_SECRET', '')
    },
    # https://console.developers.google.com/project
    "flask_social_blueprint.providers.Google": {
        # Client ID
        'consumer_key': os.environ.get('GOOGLE_KEY', ''),
        # Client secret
        'consumer_secret': os.environ.get('GOOGLE_SECRET', '')
    },
    # https://github.com/settings/applications/new
    "flask_social_blueprint.providers.Github": {
        # Client ID
        'consumer_key': os.environ.get('GITHUB_KEY', ''),
        # Client Secret
        'consumer_secret': os.environ.get('GITHUB_SECRET', '')
    },
}
