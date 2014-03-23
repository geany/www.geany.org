# -*- coding: utf-8 -*-
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

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.generic.base import TemplateView
from geany.sitemaps import GeanyDisplayableSitemap
from mezzanine.conf import settings
from nightlybuilds.views import NightlyBuildsView


sitemaps = {"sitemaps": {"all": GeanyDisplayableSitemap}}


admin.autodiscover()

urlpatterns = i18n_patterns("",
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    ("^admin/", include(admin.site.urls)),
)

if settings.USE_MODELTRANSLATION:
    urlpatterns += patterns('',
        url('^i18n/$', 'django.views.i18n.set_language', name='set_language'),
    )

# Geany patterns
urlpatterns += patterns("",
    # use our custom sitemap implementation
    url(r"^sitemap\.xml$", 'django.contrib.sitemaps.views.sitemap', sitemaps),

    # news (for now implemented using the Mezzanine blog app)
    url("^news/$", "mezzanine.blog.views.blog_post_list", name="news"),

    # TODO, NEWS, etc.
    url(r"^", include("static_docs.urls")),

    # nightly builds
    url(r"^download/nightly-builds/$", NightlyBuildsView.as_view()),

    # /service/version.php (for the UpdateChecker plugin)
    url(r"^", include("latest_version.urls")),

    # home page
    url(r"^$", TemplateView.as_view(template_name='home.html'), name='home'),

    # everything else
    url(r"^", include("mezzanine.urls")),
)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, }),
   )
