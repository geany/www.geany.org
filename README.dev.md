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

For now, the code is tested against Python2 only.


Prepare your system
-------------------

To ease package handling and to get a clean environment, we use
virtualenv. Into the virtualenv we will install Django, Mezzanine and a couple of
other helper packages.

To be able to use virtualenv, you first need to install it as well as some
development libraries for the MySQL and Memcache client libraries.
The most easy way is to use the package manager of your distribution.
On the Debian like systems the following command should install the necessary
packages:

    apt-get install python-virtualenv python-pip libmysqlclient-dev libmemcached-dev


Get the code
------------

Perform a usual clone of the www.geany.org repository from Github:

    git clone git://github.com/geany/www.geany.org


Setting up a virtualenv
-----------------------

Change into the freshly cloned repository directory and execute the following commands
to create a new virtualenv and install required Python packages:

    export PIP_REQUIRE_VIRTUALENV=true
    export VIRTUALENV_USE_DISTRIBUTE=true
    export VIRTUALENV_NO_SITE_PACKAGES=true

    virtualenv --distribute --no-site-packages venv
    # activate virtual environment
    source venv/bin/activate
    # upgrade some packages, just to be safe
    pip install --upgrade pip distribute
    # very helpful tool to manage packages in addition to pip
    pip install yolk
    # install our requirements
    pip install -r requirements.txt

This will setup a new virtualenv, upgrade the Python package manager
pip and install required packages for the website.


Create a local config
---------------------

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
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "dbname",
            "USER": "dbuser",
            "PASSWORD": "supersecret",
            "HOST": "127.0.0.1",
        },
        'nightlybuilds': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'dbname2',
            "USER": "dbuser",
            "PASSWORD": "supersecret",
            "HOST": "127.0.0.1",
        }
    }

    # some random characters, should be unique per site, e.g. use str(uuid.uuid4())
    SECRET_KEY = "12345"

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

    NIGHTLYBUILDS_BASE_DIR = '/path/to/nightlybuilds/or/just/empty/'


### Database settings ###

The above example configures a MySQL database connection.
For local development you can also use Sqlite which is simpler
to setup but harder to work with when you need to manipulate the
data directly.
Your choice.
Whatever database you use, ask Enrico to get a dump of a demo database
to get something to work with. This dump can be easily imported into
a configured database with the following command:

    python manage.py loaddata geany_dump.fixture


Start the development server
----------------------------

After you setup everything as described above, you are almost ready
to start the development server to actually do something.

Before, just one further step is required: activate your virtual environment.
Execute the following command in the directory *www.geany.org*:

    source venv/bin/activate

This will activate the previously created virtualenv and mangles
your Python environment so that the interpreter and related packages
in the *venv* sub directory are used instead of the gloablly installed
ones.
On some shells, you will see a `(venv)` prefix in the prompt indicating
a virtualenv is activated.
If you later want to clean up your shell and leave that virtualenv, just
type `deactivate` in your shell.

Now, finally, it's time to start your development server:

    python manage.py runserver

This will start a simple HTTP server on *localhost* port 8000.
You can open the resulting site in your browser by pointing it
to *http://localhost:8000*.

Basically now you are done and you can start improving the website.
A little detail you might notice: once you change any .py file
which is knwon by Django, the development server will restart automatically
to reload the changed file(s). This is very helpful.

To stop the server, simply interrupt it with *Ctrl-C*.


Special hostnames / DNS
-----------------------

Since this website project not only contains www.geany.org but also
some related subsites (pastebin.geany.org, nightly.geany.org) there is
a special DNS record on the geany.org zone: ***.local.geany.org**.

This record and all subdomains will resolve to *127.0.0.1* (aka *localhost*).

In your browser you can use http://pastebin.local.geany.org/ and
http://nightly.local.geany.org/ to use this subsites with your
local development server.
All other domains not recognized as a known subsite will fallback to
the main website.


Useful shell aliases
--------------------

No magic, just save some typing:

    alias vac='source venv/bin/activate'
    alias runserver='python manage.py runserver'
