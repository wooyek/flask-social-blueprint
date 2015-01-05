# Flask Social Blueprint example for SQLAlchemy

To run this example:

1. Map your loop back 127.0.0.1 ip address to dev.example.com
2. [Obtain client ids and secrets from OAuth providers][1] you want to integrate
3. Put them in the `website/settings.py` in the `SOCIAL_BLUEPRINT` settings
4. Install package dependencies
5. Initialize database `python manage.py initdb`
6. Run web server `python main.py`
7. Open http://dev.example.com:5055 your browser

 [1]: https://github.com/wooyek/flask-social-blueprint#setup-oauth-with-different-providers