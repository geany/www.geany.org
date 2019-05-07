# coding: utf-8
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

from __future__ import absolute_import, unicode_literals

import logging
import os

from django.utils.translation import ugettext_lazy as _


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
INTERNAL_IPS = ("127.0.0.1", "10.0.44.3", "37.120.182.205", "2a03:4000:f:40f:99::205")


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
SITE_DOMAIN_WWW = 'www.geany.org'
SITE_DOMAIN_PASTEBIN = 'pastebin.geany.org'
SITE_DOMAIN_NIGHTLY = 'nightly.geany.org'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

AUTHENTICATION_BACKENDS = ("mezzanine.core.auth_backends.MezzanineBackend",)

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB


ADMINS = (('Enrico Tröger', 'enrico.troeger@uvena.de'),)
MANAGERS = ADMINS

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
ROOT_URLCONF = "%s.urls" % PROJECT_APP

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
            'builtins': [
                'mezzanine.template.loader_tags',
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


################
# APPLICATIONS #
################

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
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
    "mezzanine.blog",
    "mezzanine.forms",
    "mezzanine.galleries",
    "mezzanine.twitter",

    # we
    "geany",
    "news",
    "latest_version",
    "static_docs",
    "pastebin",         # pastebin.geany.org
    "nightlybuilds",    # nightly.geany.org

    # 3rd party
    "honeypot",     # for pastebin
    "mezzanine_pagedown",
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
    "django.middleware.common.BrokenLinkEmailsMiddleware",
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

# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

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
    'nl2br',
    'tables',
    'toc',
)

#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    "debug_toolbar",
    "django_extensions",
    "memcache_status",
    "compressor",
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
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
        "blog.BlogPost",
        "news.NewsPost",
        "generic.ThreadedComment",
        "mezzanine_blocks.Block",
        "mezzanine_blocks.RichBlock",
        (_("Media Library"), "fb_browse"),)),
    (_("Site"), (
        "sites.Site",
        "redirects.Redirect",
        "conf.Setting",
    )),
    (_("Geany"), (
        "latest_version.LatestVersion",
    )),
    (_("Users"), ("auth.User", "auth.Group",)))

# django-debug-toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = False

# caching & sessions
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = True

# django compressor
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter']
COMPRESS_OFFLINE = True

# django-honeypot
HONEYPOT_FIELD_NAME = 'website'

NIGHTLYBUILDS_BASE_DIR = '/path/to/nightly/builds'

STATIC_DOCS_GEANY_SOURCE_DIR = '/home/geany/geany/geany_git/po'
STATIC_DOCS_GEANY_DESTINATION_DIR = os.path.join(MEDIA_ROOT, 'i18n')
STATIC_DOCS_GEANY_DESTINATION_URL = os.path.join(MEDIA_URL, 'i18n')
STATIC_DOCS_GEANY_I18N_STATISTICS_FILENAME = 'i18n_statistics.json'

IRC_USER_LIST_FILE = '/var/tmp/irc_userlist'


#########################
# LOGGING               #
#########################
logging.captureWarnings(True)  # log warnings using the logging subsystem
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(name)s %(process)d %(threadName)s %(levelname)s [%(request_id)s] %(message)s'
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
            'filters': ['require_debug_false', 'request_id']
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/srv/django/log/geany_web.log',
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


##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.

# Instead of doing "from .local_settings import *", we use exec so that
# local_settings has full access to everything defined in this module.
filename = os.path.join(PROJECT_APP_PATH, 'local_settings.py')  # pylint: disable=invalid-name
if os.path.exists(filename):
    import sys
    import imp
    module_name = '{}.local_settings'.format(PROJECT_APP)  # pylint: disable=invalid-name
    module = imp.new_module(module_name)  # pylint: disable=invalid-name
    module.__file__ = filename
    sys.modules[module_name] = module
    exec(open(filename, 'rb').read())  # pylint: disable=exec-used


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
