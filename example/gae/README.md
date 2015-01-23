# Flask Social Blueprint example for Google App Engine

To run this example:

1. Map your loop back 127.0.0.1 ip address to dev.example.com
2. [Obtain client ids and secrets from OAuth providers][1] you want to integrate
3. Put them in the `website/settings.py` in the `SOCIAL_BLUEPRINT` settings
4. Install package dependencies
5. Run app engine development server
6. Open http://dev.example.com:5055 your browser

 [1]: https://github.com/wooyek/flask-social-blueprint#setup-oauth-with-different-providers

## Google App Engine needs requirements installed in-place

The way you deploy apps to GAE you need to get everything you need inside a project directory
and import all the dependencies as local modules.

Tp simplify things a little we can install requirements into a special `lib` folder within a project directory,
then during application startup we'll put this folder on `sys.path`

Install packages here with:

    pip install --target=./lib -r requirements.txt

Or on windows:

    pip install --target=.\lib -r requirements.txt
