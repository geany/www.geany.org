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

from datetime import datetime
import json
import logging
import os.path
import re

from django.conf import settings
from django.core.cache import cache
from django.http import Http404
from django.views.generic.base import TemplateView
from mezzanine_pagedown.filters import plain as markdown_plain

from geany.decorators import (
    cache_function,
    CACHE_KEY_STATIC_DOCS_RELEASE_NOTES,
    CACHE_TIMEOUT_1HOUR,
    CACHE_TIMEOUT_24HOURS,
)
from static_docs.github_client import GitHubApiClient


RELEASE_REGEXP = re.compile(r'^Geany (?P<version>[0-9\.]+) \((?P<date>.*)\)$')
DATE_PATTERNS_TO_BE_IGNORED = ('TBD', 'TBA', 'unreleased')

CACHE_KEY_THEME_INDEX_MD5_HASH = 'THEME_INDEX_MD5_HASH'
CACHE_KEY_THEME_INDEX = 'THEME_INDEX'

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class ReleaseDto:
    """Simple data holder"""

    # ----------------------------------------------------------------------
    def __init__(self):
        self.version = None
        self.release_date = None
        self.release_notes = None

    # ----------------------------------------------------------------------
    def __repr__(self):
        return f'Geany {self.version} ({self.release_date})'


class StaticDocsView(TemplateView):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._file_contents = None

    # ----------------------------------------------------------------------
    def _fetch_file_via_github_api(self, filename, user=None, repository=None):
        client = GitHubApiClient(auth_token=settings.STATIC_DOCS_GITHUB_API_TOKEN)
        self._file_contents = client.get_file_contents(filename, user=user, repository=repository)


class ReleaseNotesView(StaticDocsView):
    """
    Grab the NEWS file from GIT master via Github API, parse it and send it back to the template
    """

    template_name = 'pages/documentation/releasenotes.html'

    # ----------------------------------------------------------------------
    def get_context_data(self, **kwargs):
        releases = self._get_release_notes()
        release = None

        version = kwargs.get('version', None)
        release = self._get_release_notes_for_version(releases, version=version)

        context = super().get_context_data(**kwargs)
        context['selected_release'] = release
        context['releases'] = releases
        return context

    # ----------------------------------------------------------------------
    @cache_function(CACHE_TIMEOUT_24HOURS, key=CACHE_KEY_STATIC_DOCS_RELEASE_NOTES)
    def _get_release_notes(self):
        self._fetch_file_via_github_api('NEWS')
        return self._parse_news_file()

    # ----------------------------------------------------------------------
    def _parse_news_file(self):
        releases = []
        current_release = None
        current_release_notes = None
        for line in self._file_contents.splitlines():
            if line.startswith('Geany'):
                version, date = self._parse_release_line(line)
                if not version or date in DATE_PATTERNS_TO_BE_IGNORED:
                    # mark for later exclusion
                    version, date = (None, None)
                # if we have a previous release already processed,
                # compress the list of lines to a string
                if current_release is not None:
                    current_release.release_notes = '\n'.join(current_release_notes)
                # make a new release
                current_release = ReleaseDto()
                current_release.version = version
                current_release.release_date = date
                releases.append(current_release)
                current_release_notes = []
            else:
                line = line.lstrip()  # remove any indentation
                if line and not line.startswith('*'):
                    # we got a section: make it bold and add an additional new line
                    # to make Markdown recognise the following lines as list
                    current_release_notes.append(f'**{line}**\n')
                else:
                    current_release_notes.append(line)

        # compress the lines of the last release (the for loop ends before)
        current_release.release_notes = '\n'.join(current_release_notes)

        # filter out releases to ignore
        releases = [release for release in releases if release.version is not None]
        return releases

    # ----------------------------------------------------------------------
    def _parse_release_line(self, line):
        match = RELEASE_REGEXP.match(line)
        if match:
            return match.group('version'), match.group('date')

        logger.warning('Failed parsing NEWS file: release line "%s" invalid', line)
        return None, None

    # ----------------------------------------------------------------------
    def _get_release_notes_for_version(self, releases, version=None):
        """
        If version is None: fetch the latest release from Github
        If version is not None:
          - check if the requested version has a release on Github and if it has release notes,
            use it
          - otherwise fetch the release notes from the already parsed NEWS file

        Finally convert the release notes from Markdown.
        """
        if version is None:
            release = self._get_release_from_github(version=None)
        else:
            # first search the release on Github
            release = self._get_release_from_github(version=version)
            if release is None:
                # fallback to the NEWS file release notes
                for rel in releases:
                    if rel.version == version:
                        release = rel
                        break
                else:
                    raise Http404()

        # convert the selected release (the one we want to display) to Markdown
        release.release_notes = markdown_plain(release.release_notes)
        return release

    # ----------------------------------------------------------------------
    @cache_function(CACHE_TIMEOUT_24HOURS)
    def _get_release_from_github(self, version=None):
        client = GitHubApiClient(auth_token=settings.STATIC_DOCS_GITHUB_API_TOKEN)
        if version is None:
            github_release = client.get_latest_release()
        else:
            tag_name = self._convert_version_to_tag_name(version)
            github_release = client.get_release_by_tag(tag_name)

        if github_release is None:
            return None

        # adapt date
        release_datetime = datetime.strptime(github_release['published_at'], '%Y-%m-%dT%H:%M:%SZ')
        release_date = release_datetime.strftime('%B %d, %Y')

        release = ReleaseDto()
        release.version = github_release['tag_name']
        release.release_date = release_date
        release.release_notes = github_release['body']
        return release

    # ----------------------------------------------------------------------
    def _convert_version_to_tag_name(self, version):
        if version.count('.') == 1:
            return f'{version}.0'

        return version


class ToDoView(StaticDocsView):
    """
    Grab the TODO file from GIT master via Github API, parse it and send it back to the template
    """

    template_name = "pages/documentation/todo.html"

    # ----------------------------------------------------------------------
    def get_context_data(self, **kwargs):
        todo = self._get_todo()
        context = super().get_context_data(**kwargs)
        context['todo'] = todo
        return context

    # ----------------------------------------------------------------------
    @cache_function(CACHE_TIMEOUT_24HOURS)
    def _get_todo(self):
        self._fetch_file_via_github_api('TODO')
        return self._parse_news_file()

    # ----------------------------------------------------------------------
    def _parse_news_file(self):
        return self._file_contents


class I18NStatisticsView(TemplateView):

    template_name = "pages/i18n.html"

    # ----------------------------------------------------------------------
    def get_context_data(self, **kwargs):
        i18n_statistics = self._get_i18n_statistics()
        context = super().get_context_data(**kwargs)
        context['i18n_statistics'] = i18n_statistics
        context['generated_datetime'] = datetime.utcfromtimestamp(
            i18n_statistics['generated_timestamp'])
        context['static_docs_geany_destination_url'] = settings.STATIC_DOCS_GEANY_DESTINATION_URL
        return context

    # ----------------------------------------------------------------------
    @cache_function(CACHE_TIMEOUT_1HOUR)
    def _get_i18n_statistics(self):
        filename = os.path.join(
            settings.STATIC_DOCS_GEANY_DESTINATION_DIR,
            settings.STATIC_DOCS_GEANY_I18N_STATISTICS_FILENAME)
        with open(filename, encoding='utf-8') as input_file:
            return json.load(input_file)


class ThemesView(StaticDocsView):
    """
    Fetch the Geany-Themes index from https://github.com/geany/geany-themes/tree/master/index
    """

    template_name = "pages/download/themes.html"

    # ----------------------------------------------------------------------
    def get_context_data(self, **kwargs):
        theme_index = self._get_theme_index()
        context = super().get_context_data(**kwargs)
        context['theme_index'] = theme_index
        return context

    # ----------------------------------------------------------------------
    def _get_theme_index(self):
        """
        Refresh the theme index by:
        - querying the MD5 hash from Github
        - compare the freshly retrieved MD5 hash against the cached one
        - load the whole theme index if:
            - the MD5 hashes differ
            - the MD5 hash was not retrieved yet or has been expired from cache
            - the theme index was not retrieved yet or has been expired from cache
        - after loading the whole theme index cache it long (24 hours)
        - store the freshly retrieved MD5 hash in the cache
        """
        theme_index_md5_hash = self._query_theme_index_md5_hash()
        cached_theme_index_md5_hash = cache.get(CACHE_KEY_THEME_INDEX_MD5_HASH)
        theme_index = cache.get(CACHE_KEY_THEME_INDEX)

        # theme index has been changed remotely?
        if theme_index_md5_hash != cached_theme_index_md5_hash or theme_index is None:
            logger.debug('Refresh theme index from Github (MD5: %s)', theme_index_md5_hash)
            # query whole theme index
            theme_index = self._query_parse_themes_index()
            # cache it for later
            cache.set(CACHE_KEY_THEME_INDEX, theme_index, CACHE_TIMEOUT_24HOURS)

        # cache MD5 hash
        cache.set(CACHE_KEY_THEME_INDEX_MD5_HASH, theme_index_md5_hash, CACHE_TIMEOUT_24HOURS)

        return theme_index

    # ----------------------------------------------------------------------
    def _query_theme_index_md5_hash(self):
        self._fetch_file_via_github_api('index/index.json.md5', repository='geany-themes')
        return self._file_contents.strip()

    # ----------------------------------------------------------------------
    def _query_parse_themes_index(self):
        self._fetch_file_via_github_api('index/index.json', repository='geany-themes')
        theme_index = json.loads(self._file_contents)
        return theme_index
