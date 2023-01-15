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

from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.generic.base import TemplateView
from django.views.i18n import set_language
from django.views.static import serve as static_serve
from mezzanine.conf import settings
import mezzanine_pagedown.urls

from geany import urls_legacy
from geany.sitemaps import GeanyMainSitemap
from nightlybuilds.views import NightlyBuildsView


# pylint: disable=invalid-name

sitemaps = {"sitemaps": {"all": GeanyMainSitemap}}


admin.autodiscover()

urlpatterns = i18n_patterns(
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    path('admin/clearcache/', include('clearcache.urls')),
    path("admin/", include(admin.site.urls)),
)

if settings.USE_MODELTRANSLATION:
    urlpatterns += (
        path('i18n/', set_language, name='set_language'),
    )

# Geany patterns
urlpatterns += (
    # use our custom sitemap implementation
    path('sitemap.xml', sitemap, sitemaps, name='django.contrib.sitemaps.views.sitemap'),

    # Release Notes, NEWS, etc.
    re_path('^', include('static_docs.urls')),

    # nightly builds
    path('download/nightly-builds/', NightlyBuildsView.as_view(), name='nightlybuilds'),

    # /service/version.php (for the UpdateChecker plugin)
    re_path('^', include('latest_version.urls')),

    # Pastebin
    path('p/', include('pastebin.urls')),

    # URL Shortener
    # path('s/', include('urlshortener.urls')),  # disabled until it is fixed for Django 4.0

    # /news/ News
    path('news/', include('news.urls')),

    # home page
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # pagedown
    path('pagedown/', include(mezzanine_pagedown.urls)),

    # legacy URLs (redirect for old website deeplinks)
    re_path('^', include(urls_legacy)),

    # everything else
    re_path('^', include('mezzanine.urls')),
)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = 'mezzanine.core.views.page_not_found'
handler500 = 'mezzanine.core.views.server_error'


if settings.DEBUG:
    urlpatterns += (
        path('media/<path>/', static_serve, {'document_root': settings.MEDIA_ROOT, }),)
