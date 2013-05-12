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
from django.contrib import admin

from mezzanine.conf import settings
from geany.sitemaps import GeanyDisplayableSitemap
from nightlybuilds.views import NightlyBuildsView


sitemaps = {"sitemaps": {"all": GeanyDisplayableSitemap}}


admin.autodiscover()


urlpatterns = patterns("",
    url(r"^admin/", include(admin.site.urls)),

    # use our custom sitemap implementation
    url(r"^sitemap\.xml$", 'django.contrib.sitemaps.views.sitemap', sitemaps),

    url("^$", "mezzanine.blog.views.blog_post_list", name="home"),

    # TODO, NEWS, etc.
    url(r"^", include("static_docs.urls")),

    # nightly builds
    url(r"^download/nightly-builds/$", NightlyBuildsView.as_view()),

    # /service/version.php (for the UpdateChecker plugin)
    url(r"^", include("latest_version.urls")),

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
