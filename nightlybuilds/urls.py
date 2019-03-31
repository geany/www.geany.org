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

from django.conf.urls import url

from geany.sitemaps import StaticSitemap
from nightlybuilds.views import NightlyBuildsView


urlpatterns = [
    # no admin on this site
    url(r'^admin/', 'mezzanine.core.views.page_not_found'),

    url(r'^$', NightlyBuildsView.as_view(), name='home'),
]

# Sitemap framework
sitemaps = {"sitemaps": {"all": StaticSitemap('nightly.geany.org', urlpatterns)}}
urlpatterns += (
    # use our custom sitemap implementation
    url(r"^sitemap\.xml$", 'django.contrib.sitemaps.views.sitemap', sitemaps),
)
