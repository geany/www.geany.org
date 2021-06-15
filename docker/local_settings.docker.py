# coding.: utf-8

# This file is exec'd from settings.py, so it has access to and can modify all
# the variables in settings.py.

# If this file is changed in development, the development server will have to
# be manually restarted because changes will not be noticed immediately.


DEBUG = True


INTERNAL_IPS = ("127.0.0.1",)
ALLOWED_HOSTS = ('127.0.0.1', 'localhost')

STATIC_ROOT = '/app/static'
MEDIA_ROOT = '/app/docker/data'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(MEDIA_ROOT, 'geany_dev.db'),
    },
    'nightlybuilds': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(MEDIA_ROOT, 'geany_dev_nightlybuilds.db')
    }
}

SECRET_KEY = "f94b410d-0401-4f25-a69e-d5cbbf7717f3-1af070a9-ebef-4efe-a779-a9706bbdfd4a"
NEVERCACHE_KEY = "c8eb09b7-bd7e-4375-8293-6ffe53bf92e1-884d109e-6da4-4b99-bc56-075d8a498d4c"

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = False
SSL_FORCE_URL_PREFIXES = ()
SESSION_COOKIE_SECURE = False
USE_X_FORWARDED_HOST = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

FORCE_SCRIPT_NAME = ''
SERVER_EMAIL = 'root@localhost'
DEFAULT_FROM_EMAIL = 'root@localhost'

NIGHTLYBUILDS_BASE_DIR = os.path.join(MEDIA_ROOT, 'nightly_mirror')

STATIC_DOCS_GEANY_SOURCE_TARBALL = '/tmp/geany_git.tar.gz'
STATIC_DOCS_GEANY_DESTINATION_DIR = os.path.join(MEDIA_ROOT, 'i18n')
STATIC_DOCS_GEANY_DESTINATION_URL = os.path.join(MEDIA_URL, 'i18n')
STATIC_DOCS_GEANY_I18N_STATISTICS_FILENAME = 'i18n_statistics.json'

LATEST_VERSION_RELEASES_DIRECTORY = '/nonexistant/geany'
LATEST_VERSION_PLUGINS_RELEASES_DIRECTORY = '/nonexistant/plugins'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(name)s %(process)d %(threadName)s %(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers':['console'],
            'level':'DEBUG',
            'propagate': False,
        },
        'root': {
            'handlers':['console'],
            'level':'DEBUG',
            'propagate': False,
        },
        'py.warnings': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django.db': {
            'handlers':['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.template': {
            'handlers':['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.utils.autoreload': {
            'handlers': [],
            'level': 'INFO',
            'propagate': True,
        },
        'MARKDOWN': {
            'level': 'INFO',
            'propagate': True,
        },
        'PIL': {
            'handlers': [],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
