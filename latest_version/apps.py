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

from django.apps import AppConfig


class LatestVersionAppConfig(AppConfig):
    name = 'latest_version'
    verbose_name = "LatestVersion"

    # ----------------------------------------------------------------------
    def ready(self):
        # register our urlpatterns to the global sitemap generator
        # pylint: disable=import-outside-toplevel
        from geany.sitemaps import sitemap_registry, StaticSitemap
        from latest_version.urls import urlpatterns
        sitemap_registry.add(StaticSitemap, urlpatterns, exclude_views=['latest_version_legacy'])
