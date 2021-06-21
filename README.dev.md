www.geany.org - Dev Environment
===============================

About
-----
This document describes the process of setting up a development environment to
get a local instance of this website running.

The website is implemented as a Django (https://www.djangoproject.com/) project
and uses Mezzanine (http://mezzanine.jupo.org/) for content management.

As Django is based on Python, first of all you need Python and a couple of
extra packages installed on your system.

The code requires Python 3.6 or higher.

All Python related dependencies are listed in `requirements.txt` and can
be installed via `pip` (see below).
Unfortunately, the last official release of the used CMS Mezzanine supports
only Django up to 2.0. To use more recent versions of Django, the `requirements.txt`
refers to a development branch of Mezzanine (and its dependencies
filebrowser-safe and grappelli-safe) with support for Django 2.2.
Ideally, a new official Mezzanine release will obsolete the need to
depend on branches instead releases.

Get the code
------------

Perform a usual clone of the www.geany.org repository from Github:

    git clone git://github.com/geany/www.geany.org


Local setup using virtualenv
----------------------------

### Prepare your system

To ease package handling and to get a clean environment, we use
virtualenv. Into the virtualenv we will install Django, Mezzanine and a couple of
other helper packages.

To be able to use virtualenv, you first need to install it as well as some
development libraries for Python, the MySQL and Memcache client libraries.
The most easy way is to use the package manager of your distribution.
On Debian like systems the following command should install the necessary
packages:

    apt-get install python3-venv python3-pip python3-dev build-essential libmysqlclient-dev libmemcached-dev


### Setting up a virtualenv

Change into the freshly cloned repository directory and execute the following commands
to create a new virtualenv and install required Python packages:

    python3 -m venv venv
    # upgrade some packages, just to be safe
    venv/bin/pip install --upgrade pip setuptools
    # install our requirements
    venv/bin/pip install -r requirements.txt

This will setup a new virtualenv, upgrade the Python package manager
pip and install required packages for the website.


### Create a local config

Use a text editor of choice (we all know what this would be...) and create a new file
*local_settings.py* in *www.geany.org/geany/* (next to the existing *settings.py*).

Django will first read *settings.py* and then overwrite all settings found in
*local_settings.py*. This way you can adjust the installation to your needs.
Also, some sensitive settings like the database connection are not properly
configured in *settings.py* on purpose, so you **must** configure them
locally.

You can use the following sample *local_settings.py* as a start and then adjust
the settings to your needs:

    DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'geany_dev_www.db'),
        },
        'nightlybuilds': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'geany_dev_nightly.db'),
        }
    }

    # some random characters, should be unique per site, e.g. use str(uuid.uuid4())
    SECRET_KEY = "change-me-to-something-random-and-unique"
    NEVERCACHE_KEY = "change-me-to-something-random-and-unique"

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

    NIGHTLYBUILDS_BASE_DIR = '/path/to/nightlybuilds/or/just/empty/'
    # disable security on 127.0.0.1 without HTTPS
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    SSL_FORCE_URL_PREFIXES = ()
    INTERNAL_IPS = ("127.0.0.1",)
    ALLOWED_HOSTS = ('127.0.0.1', 'localhost')

    LOGGING['handlers']['file']['filename'] = '/tmp/geany_django.log'

    LATEST_VERSION_RELEASES_DIRECTORY = '/path/to/geany/releases/directory/or/just/empty'
    LATEST_VERSION_PLUGINS_RELEASES_DIRECTORY = '/path/to/plugins/releases/directory/or/just/empty'
    STATIC_DOCS_GEANY_SOURCE_TARBALL = '/path/to/geany/source/tarball/or/just/empty'


### Database settings

The above example configures a MySQL database connection.
For local development you can also use Sqlite which is simpler
to setup but harder to work with when you need to manipulate the
data directly.
Your choice.
A dump of a demo database to get something to work with is available in
`database.json`.
This dump can be easily imported into
a configured database with the following command:

    venv/bin/python manage.py reset_db --noinput
    venv/bin/python manage.py migrate --run-syncdb --noinput
    echo 'DELETE FROM auth_permission;
          DELETE FROM django_content_type;
          DELETE FROM django_site;' | venv/bin/python manage.py dbshell
    venv/bin/python manage.py loaddata database.json

The database dump contains a default admin user:

    username: admin
    password: change-me


### Start the development server

After you set up everything as described above, you are ready
to start the development server to actually do something:

    venv/bin/python manage.py runserver

This will start a simple HTTP server on *localhost* port 8000.
You can open the resulting site in your browser by pointing it
to http://localhost:8000.

Basically now you are done and you can start improving the website.
A little detail you might notice: once you change any .py file
which is knwon by Django, the development server will restart automatically
to reload the changed file(s). This is very helpful.

To stop the server, simply interrupt it with *Ctrl-C*.


Local setup using Docker
------------------------

Alternatively, a Dockerfile is provided to build a Docker image
and to run the website in a Docker container.
This is the easiest way to get a local environment running.

### Local config

When using the Docker image, a prepared local settings file is
used with already adjusted settings for running in a Docker container.
This file is located at `docker/local_settings.docker.py`.


### Build container image

First, you need to build the image:

    make docker-build

This will take some time but is only necessary once.

Note: before building the image, carefully review the Dockerfile
and especially make sure you use a base image you can trust.


### Start the container

After the image is built, you can start the container:

    make docker-run

On the first run, the database is setup, screenshots are downloaded to be
locally available as well as a few more preparations.

Once running, you can open the resulting site in your browser by pointing it
to http://localhost:8000.

Basically now you are done and you can start improving the website.
A little detail you might notice: once you change any .py file
which is knwon by Django, the development server will restart automatically
to reload the changed file(s). This is very helpful.

To stop the container, simply interrupt it with *Ctrl-C*.

### Cleanup

All files created on first container startup are stored in `docker/data`.
To start from scratch (e.g. with a fresh database, no uploads, etc.), simply
delete this directory or run:

    make docker-clean


Management Commands
-------------------

In addition to the usual Django management commands (for a
list run `python manage.py`), the Geany apps provide a few more.

### manage.py dump_database

This command will dump the configured database to a file
named `database.json` in the current directory.
The generated dump is not a SQL dump but consists of JSON
objects of all models known to Django. Only a few models
are excluded:

 * `auth.user` (excluded for privacy reasons)
 * `sessions.session` (excluded for privacy reasons)
 * `admin.logentry` (excluded for privacy reasons)
 * `pastebin.snippet` (might be much data)

The resulting dump might be used to populate a development
environment from scratch and is also committed to the
repository for general availability.


### manage.py cleanup_snippets

Clean all expired snippets in the integrated Pastebin app.
Usually, you don't need to call this command as expired
snippets will be cleaned automatically when the snippet list
is accessed via the website.


### manage.py generate_snippets_css

Update the necessary CSS classes for displaying snippet
highlighting in the Pastebin app.
The CSS classes are generated by Pygments which is used
for highlighting the snippet code in HTML.

Call this command after updates of the Pygments package and
then commit the updated CSS file `pastebin/static/css/pygments.css`.


### manage.py generate_i18n_statistics

Generate translation statistics by extracting them from the
PO files of a Geany source. These statistics are shown on the
website on /contribute/translation/statistics/.


Useful shell aliases
--------------------

No magic, just save some typing:

    alias vac='source venv/bin/activate'
    alias runserver='python manage.py runserver'
