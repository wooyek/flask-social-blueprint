# Flask Social Blueprint example

To run this example:

1. Map your loop back 127.0.0.1 ip address to dev.example.com
2. Obtain client ids and secrets from OAuth providers using URL:
   http://dev.example.com:5055 and callbacks:
    - http://dev.example.com:5055/_social/callback/Google
    - http://dev.example.com:5055/_social/callback/Facebook
    - http://dev.example.com:5055/_social/callback/Twitter
    - http://dev.example.com:5055/_social/callback/Github
3. Put them in the `website/settings.py` in the `SOCIAL_BLUEPRINT` settings
4. Install package dependencies
5. Initialize database `python manage.py initdb`
5. Run web server `python main.py`
6. Open <http://dev.example.com:5055> your browser

## Twitter

Create new appliaction here: <https://apps.twitter.com/app/new>

## Google

1. Create new project here: <https://console.developers.google.com/project>
2. In APIs & auth > Credentials create Client ID
3. Update consent screen details, at least product name, home page and email address

## Github

Create new application here: <https://github.com/settings/applications/new>

## Facebook

Create new application here: <https://developers.facebook.com/apps/>

Setup `Valid OAuth redirect URIs` in Settings > Advanced > Security

# Development environment setup for beginners

## Linux

```
sudo apt-get install python
sudo apt-get install python-dev
sudo apt-get install python-pip
sudo pip install virtualenv
```

## Windows

Install [python 2.7](https://www.python.org/download/releases/2.7/).
To quickly setup python start powershell and paste this script

    (new-object System.Net.WebClient).DownloadFile("https://www.python.org/ftp/python/2.7.6/python-2.7.6.msi", "$pwd\python-2.7.6.msi"); msiexec /i python-2.7.6.msi TARGETDIR=C:\Python27
    [Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Python27\;C:\Python27\Scripts\", "User")

Install [Pip](http://pip.readthedocs.org/en/latest/installing.html) using powershell

    (new-object System.Net.WebClient).DownloadFile("https://raw.github.com/pypa/pip/master/contrib/get-pip.py", "$pwd\get-pip.py"); C:\Python27\python.exe get-pip.py virtualenv

or using python itself

    python -c "exec('try: from urllib2 import urlopen \nexcept: from urllib.request import urlopen');f=urlopen('https://raw.github.com/pypa/pip/master/contrib/get-pip.py').read();exec(f)"

## Virtualenv

Create and [activate virtual environment](http://virtualenv.readthedocs.org/en/latest/virtualenv.html#activate-script)

    pip install -r requirements

