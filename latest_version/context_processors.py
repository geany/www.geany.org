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

from mezzanine.conf import settings

from geany.decorators import (
    cache_function,
    CACHE_KEY_LATEST_VERSION_LATEST_VERSION,
    CACHE_TIMEOUT_1HOUR,
)
from latest_version.models import LatestVersion
from latest_version.releases import ReleaseVersionsProvider


# ----------------------------------------------------------------------
@cache_function(CACHE_TIMEOUT_1HOUR, key=CACHE_KEY_LATEST_VERSION_LATEST_VERSION)
def latest_version(request):
    latest_versions = LatestVersion.objects.all()
    latest_versions_by_name = {
        latest_version.name: latest_version
        for latest_version
        in latest_versions}
    geany_latest_version = latest_versions_by_name.get('Geany')
    geany_plugins_latest_version = latest_versions_by_name.get('Geany-Plugins')

    # Geany
    release_versions_provider = ReleaseVersionsProvider(
        settings.LATEST_VERSION_RELEASES_DIRECTORY,
        fallback_version=geany_latest_version.version)
    release_versions = release_versions_provider.provide()
    # Geany-Plugins
    geany_plugins_release_versions_provider = ReleaseVersionsProvider(
        settings.LATEST_VERSION_PLUGINS_RELEASES_DIRECTORY,
        fallback_version=geany_plugins_latest_version.version)
    plugins_release_versions = geany_plugins_release_versions_provider.provide()

    return {
        'geany_latest_version': geany_latest_version,
        'geany_plugins_latest_version': geany_plugins_latest_version,
        'release_versions': release_versions,
        'plugins_release_versions': plugins_release_versions,
    }
