# LICENCE: This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import warnings

from django.utils.translation import gettext_lazy as _
from markdown.extensions.toc import TocExtension


######################
# MEZZANINE SETTINGS #
######################

# The following settings are already defined with default values in
# the ``defaults.py`` module within each of Mezzanine's apps, but are
# common enough to be put here, commented out, for conveniently
# overriding. Please consult the settings documentation for a full list
# of settings Mezzanine implements:
# http://mezzanine.jupo.org/docs/configuration.html#default-settings

# Controls the ordering and grouping of the admin menu.
#
# ADMIN_MENU_ORDER = (
#     ("Content", ("pages.Page", "blog.BlogPost",
#        "generic.ThreadedComment", (_("Media Library"), "fb_browse"),)),
#     ("Site", ("sites.Site", "redirects.Redirect", "conf.Setting")),
#     ("Users", ("auth.User", "auth.Group",)),
# )

# A three item sequence, each containing a sequence of template tags
# used to render the admin dashboard.
#
# DASHBOARD_TAGS = (
#     ("blog_tags.quick_blog", "mezzanine_tags.app_list"),
#     ("comment_tags.recent_comments",),
#     ("mezzanine_tags.recent_actions",),
# )

# A sequence of templates used by the ``page_menu`` template tag. Each
# item in the sequence is a three item sequence, containing a unique ID
# for the template, a label for the template, and the template path.
# These templates are then available for selection when editing which
# menus a page should appear in. Note that if a menu template is used
# that doesn't appear in this setting, all pages will appear in it.

# PAGE_MENU_TEMPLATES = (
#     (1, _("Top navigation bar"), "pages/menus/dropdown.html"),
#     (2, _("Left-hand tree"), "pages/menus/tree.html"),
#     (3, _("Footer"), "pages/menus/footer.html"),
# )

# A sequence of fields that will be injected into Mezzanine's (or any
# library's) models. Each item in the sequence is a four item sequence.
# The first two items are the dotted path to the model and its field
# name to be added, and the dotted path to the field class to use for
# the field. The third and fourth items are a sequence of positional
# args and a dictionary of keyword args, to use when creating the
# field instance. When specifying the field class, the path
# ``django.models.db.`` can be omitted for regular Django model fields.
#
# EXTRA_MODEL_FIELDS = (
#     (
#         # Dotted path to field.
#         "mezzanine.blog.models.BlogPost.image",
#         # Dotted path to field class.
#         "somelib.fields.ImageField",
#         # Positional args for field class.
#         (_("Image"),),
#         # Keyword args for field class.
#         {"blank": True, "upload_to": "blog"},
#     ),
#     # Example of adding a field to *all* of Mezzanine's content types:
#     (
#         "mezzanine.pages.models.Page.another_field",
#         "IntegerField", # 'django.db.models.' is implied if path is omitted.
#         (_("Another name"),),
#         {"blank": True, "default": 1},
#     ),
# )

# Setting to turn on featured images for blog posts. Defaults to False.
#
# BLOG_USE_FEATURED_IMAGE = True

# If ``True``, users will be automatically redirected to HTTPS
# for the URLs specified by the ``SSL_FORCE_URL_PREFIXES`` setting.
#
# SSL_ENABLED = True  # managed via dynamic settings in the Django Admin

# Host name that the site should always be accessed via that matches
# the SSL certificate.
#
# SSL_FORCE_HOST = "www.example.com"

# Sequence of URL prefixes that will be forced to run over
# SSL when ``SSL_ENABLED`` is ``True``. i.e.
# ('/admin', '/example') would force all URLs beginning with
# /admin or /example to run over SSL. Defaults to:
#
SSL_FORCE_URL_PREFIXES = ("/admin", "/account")

# Django security settings
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

X_FRAME_OPTIONS = 'DENY'

# If True, the django-modeltranslation will be added to the
# INSTALLED_APPS setting.
USE_MODELTRANSLATION = False

USE_X_FORWARDED_HOST = True


########################
# MAIN DJANGO SETTINGS #
########################

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ('127.0.0.1',
                 'geany.org',
                 'www.geany.org')
INTERNAL_IPS = ('127.0.0.1', '10.0.44.3')

SECRET_KEY = 'change-me'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# If you set this to True, Django will use timezone-aware datetimes.
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en"

# Supported languages
LANGUAGES = (
    ('en', _('English')),
)

# A boolean that turns on/off debug mode. When set to ``True``, stack traces
# are displayed for error pages. Should always be set to ``False`` in
# production. Best set to ``True`` in local_settings.py
DEBUG = False

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

AUTHENTICATION_BACKENDS = ("mezzanine.core.auth_backends.MezzanineBackend",)

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB


ADMINS = (('Enrico Tröger', 'webmaster@geany.org'),)
MANAGERS = ADMINS
SERVER_EMAIL = 'webmaster@geany.org'
DEFAULT_FROM_EMAIL = 'webmaster@geany.org'

#############
# DATABASES #
#############

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "dbname",
        "USER": "",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_ALL_TABLES'; SET storage_engine=INNODB"
        },
    },
    'nightlybuilds': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dbname',
        "USER": "",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_ALL_TABLES';"
        },
    }
}
DATABASE_ROUTERS = ['nightlybuilds.database_routers.NightlyBuildsRouter']

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


#########
# PATHS #
#########

# Full filesystem path to the project.
PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_APP = os.path.basename(PROJECT_APP_PATH)
PROJECT_ROOT = BASE_DIR = os.path.dirname(PROJECT_APP_PATH)

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_APP
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_MIDDLEWARE_ALIAS = 'default'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))

# Package/module name to import the root urlpatterns from for the project.
ROOT_URLCONF = f'{PROJECT_APP}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(PROJECT_APP_PATH, "templates"),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.tz',
                'mezzanine.conf.context_processors.settings',
                'latest_version.context_processors.latest_version',
                'mezzanine.pages.context_processors.page',
            ],
        },
    },
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'compressor.finders.CompressorFinder',
)

# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

################
# APPLICATIONS #
################

INSTALLED_APPS = (
    "clearcache",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.pages",
    "mezzanine.forms",
    "mezzanine.galleries",

    # we
    "geany.apps.GeanyAppConfig",
    "news.apps.NewsAppConfig",
    "latest_version.apps.LatestVersionAppConfig",
    "static_docs.apps.StaticDocsAppConfig",
    "pastebin.apps.PastebinAppConfig",
    "nightlybuilds.apps.NightlyBuildsAppConfig",
    "urlshortener.apps.UrlShortenerAppConfig",

    # 3rd party
    "compressor",
    "django_extensions",
    "mezzanine_pagedown",
    "mezzanine_sync_pages.apps.MezzanineSyncPagesAppConfig",
    # "shortener",  # disabled until it is fixed for Django 4.0 or we remove it completely
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

# List of middleware classes to use. Order is important; in the request phase,
# these middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE = (
    "log_request_id.middleware.RequestIDMiddleware",
    "mezzanine.core.middleware.UpdateCacheMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # Uncomment if using internationalisation or localisation
    # "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.RedirectFallbackMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    "mezzanine.core.middleware.SitePermissionMiddleware",
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
    "mezzanine.core.middleware.FetchFromCacheMiddleware",
)

# pagedown / markdown
RICHTEXT_WIDGET_CLASS = 'mezzanine_pagedown.widgets.PageDownWidget'
RICHTEXT_FILTERS = ['mezzanine_pagedown.filters.custom']
RICHTEXT_FILTER_LEVEL = 3
PAGEDOWN_SERVER_SIDE_PREVIEW = False
PAGEDOWN_MARKDOWN_EXTENSIONS = (
    # GFM alike
    'pymdownx.magiclink',
    'pymdownx.betterem',
    'pymdownx.tilde',
    'pymdownx.tasklist',
    'pymdownx.superfences',
    # markdown extensions
    'footnotes',
    'nl2br',
    'tables',
    # create TOC entries only for heading level 2 to 4
    # level 1 usually is the page header, we don't need levels deeper than 4
    TocExtension(toc_depth='2-4'),
)

#########################
# GEANY SETINGS         #
#########################

# some more Mezzanine settings
FORMS_USE_HTML5 = True
INLINE_EDITING_ENABLED = False

# dashboard
DASHBOARD_TAGS = (
    ("mezzanine_tags.app_list",),
    ("mezzanine_tags.recent_actions",),
    ("comment_tags.recent_comments",),
)

ADMIN_MENU_ORDER = (
    (_("Content"), (
        "pages.Page",
        "news.NewsPost",
        "generic.ThreadedComment",
        "mezzanine_blocks.Block",
        "mezzanine_blocks.RichBlock",
        "mezzanine_sync_pages.MezzanineSyncPages",
        (_("Media Library"), "fb_browse"),)),
    (_("Site"), (
        "sites.Site",
        "redirects.Redirect",
        "conf.Setting",
        (_("Clear Cache"), "clearcache_admin"),
    )),
    (_("Geany"), (
        "latest_version.LatestVersion",
    )),
    (_("Users"), ("auth.User", "auth.Group",)))  # pylint: disable=hard-coded-auth-user

# caching & sessions
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = True

# django compressor
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter']
COMPRESS_OFFLINE = True

NIGHTLYBUILDS_BASE_DIR = '/path/to/nightly/builds'

STATIC_DOCS_GITHUB_API_TOKEN = None
STATIC_DOCS_GEANY_SOURCE_TARBALL = '/srv/www/download.geany.org/geany_git.tar.gz'
STATIC_DOCS_GEANY_DESTINATION_DIR = os.path.join(MEDIA_ROOT, 'i18n')
STATIC_DOCS_GEANY_DESTINATION_URL = os.path.join(MEDIA_URL, 'i18n')
STATIC_DOCS_GEANY_I18N_STATISTICS_FILENAME = 'i18n_statistics.json'

LATEST_VERSION_RELEASES_DIRECTORY = '/srv/www/download.geany.org'
LATEST_VERSION_PLUGINS_RELEASES_DIRECTORY = '/srv/www/plugins.geany.org/geany-plugins/'

MEZZANINE_SYNC_PAGES_DESTINATION_PATH = os.path.join(PROJECT_ROOT, 'page_content')


#########################
# LOGGING               #
#########################
def skip_404_not_found(record):
    # filter 404 Not Found log messages and ignore them to prevent sending lots of mails
    # via AdminEmailHandler
    if record.name == 'django.request' and getattr(record, 'status_code', 0) == 404:
        return False
    return True


logging.captureWarnings(True)  # log warnings using the logging subsystem
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
                '%(asctime)s %(name)s %(process)d %(threadName)s '
                '%(levelname)s [%(request_id)s] %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        },
        'skip_404_not_found': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_404_not_found,
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true', 'request_id'],
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'WARN',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false', 'request_id', 'skip_404_not_found']
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'geany_web.log',
            'filters': ['request_id'],
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'root': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': [],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django': {
            'handlers': [],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'handlers': [],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends.schema': {
            'handlers': [],
            'level': 'INFO',
            'propagate': True,
        },
        'django.server': {
            'handlers': [],
            'level': 'INFO',
            'propagate': True,
        },
        'django.security': {
            'handlers': [],
            'level': 'INFO',
            'propagate': True,
        },
        'django.template': {
            'handlers': [],
            'level': 'INFO',
            'propagate': True,
        },
        'django.utils.autoreload': {
            'handlers': [],
            'level': 'INFO',
            'propagate': True,
        },
        'MARKDOWN': {
            'handlers': [],
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
# add "request_id" attribute to log records (read from the header set by the webserver)
GENERATE_REQUEST_ID_IF_NOT_IN_HEADER = False
LOG_REQUEST_ID_HEADER = 'HTTP_REQUEST_ID'
LOG_REQUESTS = False


###################
# IGNORE WARNINGS #
###################
SILENCED_SYSTEM_CHECKS = (
)
# ignore warnings we cannot fix:
# FutureWarning: mezzanine/core/templatetags/mezzanine_tags.py:492:
# mezzanine_pagedown.filters.custom needs to ensure that any untrusted inputs are properly escaped
warnings.filterwarnings(
    action='ignore',
    message='^mezzanine_pagedown.filters.custom needs to ensure that any untrusted inputs.*',
    category=FutureWarning,
    module='mezzanine.core.templatetags.mezzanine_tags',
    lineno=494)


##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.

# Instead of doing "from .local_settings import *", we use exec so that
# local_settings has full access to everything defined in this module.
# pylint: disable=invalid-name
local_settings_file_name = os.environ.get('LOCAL_SETTINGS_PY', 'local_settings.py')
filename = os.path.join(PROJECT_APP_PATH, local_settings_file_name)  # pylint: disable=invalid-name
if os.path.exists(filename):
    from importlib.util import module_from_spec, spec_from_file_location
    import sys
    module_name = f'{PROJECT_APP}.local_settings'  # pylint: disable=invalid-name
    spec = spec_from_file_location(module_name, filename)  # pylint: disable=invalid-name
    module = module_from_spec(spec)  # pylint: disable=invalid-name
    sys.modules[module_name] = module
    with open(filename, 'rb') as local_config:
        exec(local_config.read())  # pylint: disable=exec-used


####################
# DYNAMIC SETTINGS #
####################

# set_dynamic_settings() will rewrite globals based on what has been
# defined so far, in order to provide some better defaults where
# applicable. We also allow this settings module to be imported
# without Mezzanine installed, as the case may be when using the
# fabfile, where setting the dynamic settings below isn't strictly
# required.
try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())
