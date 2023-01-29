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

from pathlib import Path
import logging
import re

from django.conf import settings
from packaging.version import parse as parse_version


RELEASE_TYPE_SOURCE_GZIP = 'source_gzip_version'
RELEASE_TYPE_SOURCE_BZIP2 = 'source_bzip2_version'
RELEASE_TYPE_WINDOWS = 'windows_version'
RELEASE_TYPE_MACOS = 'macos_version'
RELEASE_TYPE_MACOS_ARM64 = 'macos_version_arm64'

RELEASE_TYPES = {
    settings.LATEST_VERSION_RELEASES_DIRECTORY: {
        RELEASE_TYPE_SOURCE_GZIP: {
            'pattern': re.compile(r'^geany-([0-9\.\-]+).tar.gz$'),
            'fallback_filename': 'geany-{version}.tar.gz'
        },
        RELEASE_TYPE_SOURCE_BZIP2: {
            'pattern': re.compile(r'^geany-([0-9\.\-]+).tar.bz2$'),
            'fallback_filename': 'geany-{version}.tar.bz2'
        },
        RELEASE_TYPE_WINDOWS: {
            'pattern': re.compile(r'^geany-([0-9\.\-]+)_setup(-[0-9]+)?.exe$'),
            'fallback_filename': 'geany-{version}_setup.exe'
        },
        RELEASE_TYPE_MACOS: {
            'pattern': re.compile(r'^geany-([0-9\.\-]+)_osx(-[0-9]+)?.dmg$'),
            'fallback_filename': 'geany-{version}_osx.dmg'
        },
        RELEASE_TYPE_MACOS_ARM64: {
            'pattern': re.compile(r'^geany-([0-9\.\-]+)_osx_arm64(-[0-9]+)?.dmg$'),
            'fallback_filename': 'geany-{version}_osx_arm64.dmg'
        },
    },

    settings.LATEST_VERSION_PLUGINS_RELEASES_DIRECTORY: {
        RELEASE_TYPE_SOURCE_GZIP: {
            'pattern': re.compile(r'^geany-plugins-([0-9\.\-]+).tar.gz$'),
            'fallback_filename': 'geany-plugins-{version}.tar.gz'
        },
        RELEASE_TYPE_SOURCE_BZIP2: {
            'pattern': re.compile(r'^geany-plugins-([0-9\.\-]+).tar.bz2$'),
            'fallback_filename': 'geany-plugins-{version}.tar.bz2'
        },
        RELEASE_TYPE_WINDOWS: {
            'pattern': re.compile(r'^geany-plugins-([0-9\.\-]+)_setup(-[0-9]+)?.exe$'),
            'fallback_filename': 'geany-plugins-{version}_setup.exe'
        },
    },
}


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class ReleaseVersions:

    source_gzip_version = None
    source_bzip2_version = None
    windows_version = None
    macos_version = None
    macos_version_arm64 = None


class ReleaseVersionsProvider:

    # ----------------------------------------------------------------------
    def __init__(self, releases_directory, fallback_version):
        self._releases_directory = releases_directory
        self._fallback_version = fallback_version
        self._release_files = None
        self._release_files_by_version = None
        self._release_versions = None

    # ----------------------------------------------------------------------
    def provide(self):
        self._fetch_releases_from_filesystem()
        self._group_releases_by_type()
        self._factor_release_versions()

        return self._release_versions

    # ----------------------------------------------------------------------
    def _fetch_releases_from_filesystem(self):
        self._release_files = []

        if not self._releases_directory:
            return

        path = Path(self._releases_directory)
        if not path.exists():
            return

        for entry in path.iterdir():
            relative_entry = entry.relative_to(self._releases_directory)
            filename = relative_entry.as_posix()
            self._release_files.append(filename)

    # ----------------------------------------------------------------------
    def _group_releases_by_type(self):
        self._release_files_by_version = {}
        release_types = self._get_release_types()
        for release_type in release_types:
            self._release_files_by_version[release_type] = []

        for filename in self._release_files:
            for release_type in release_types:
                match = release_types[release_type]['pattern'].match(filename)
                if match:
                    version = ''.join([part for part in match.groups() if part])
                    self._release_files_by_version[release_type].append((filename, version))
                    break

    # ----------------------------------------------------------------------
    def _get_release_types(self):
        return RELEASE_TYPES.get(self._releases_directory, {})

    # ----------------------------------------------------------------------
    def _factor_release_versions(self):
        self._release_versions = ReleaseVersions()
        for release_type in self._release_files_by_version:
            latest_version = self._determine_latest_version(release_type)

            setattr(self._release_versions, release_type, latest_version)

    # ----------------------------------------------------------------------
    def _determine_latest_version(self, release_type):
        versions = self._release_files_by_version[release_type]
        sorted_versions = sorted(versions, key=self._parse_version)
        release_types = self._get_release_types()
        try:
            latest_version = sorted_versions.pop()
            latest_version_filename, _ = latest_version
            logger.debug('Latest version found for "%s": %s', release_type, latest_version_filename)
        except IndexError:
            fallback_filename = release_types[release_type]['fallback_filename']
            latest_version_filename = fallback_filename.format(version=self._fallback_version)
            logger.debug(
                'Latest version found for "%s": %s (fallback)',
                release_type, latest_version_filename)

        return latest_version_filename

    # ----------------------------------------------------------------------
    def _parse_version(self, version):
        _, version_number = version
        return parse_version(version_number)
