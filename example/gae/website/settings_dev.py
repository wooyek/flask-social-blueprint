# coding=utf-8
# Created 2014 by Janusz Skonieczny 

# Flask-SocialBlueprint
# https://github.com/wooyek/flask-social-blueprint
SOCIAL_BLUEPRINT = {
    # https://developers.facebook.com/apps/
    "flask_social_blueprint.providers.Facebook": {
        # App ID
        'consumer_key': '784976584887745',
        # Client Token
        'consumer_secret': 'dea85fa85a1e648261913dfe35248231'
    },
    # https://apps.twitter.com/app/new
    "flask_social_blueprint.providers.Twitter": {
        # Your access token from API Keys tab
        'consumer_key': 'FDUpwXwc57yhK2pc5x2LYDCxf',
        # access token secret
        'consumer_secret': 'oRgvj3sYfw3Kqr7i3Bn9hYT4Umifo3qeNGViHcNac48DtWLXtb'
    },
    # https://console.developers.google.com/project
    "flask_social_blueprint.providers.Google": {
        # Client ID
        'consumer_key': '1028416535138-nk697mk4aeqkrof18of9dc5dia6lhbqv.apps.googleusercontent.com',
        # Client secret
        'consumer_secret': 'lDdFchAY6dRAB9VGquZOUnVz'
    },
    # https://github.com/settings/applications/new
    "flask_social_blueprint.providers.Github": {
        # Client ID
        'consumer_key': '07a41e7d83ff2ae61ec1',
        # Client Secret
        'consumer_secret': 'da65f157cebe1edcef26cc278370ac26715826c0'
    },
}
