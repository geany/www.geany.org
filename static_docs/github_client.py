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

# try to get any json implementation
from base64 import standard_b64decode
import logging
import requests


GITHUB_API_URL = 'https://api.github.com/'
GITHUB_USER = 'geany'
GITHUB_REPOSITORY = 'geany'
HTTP_REQUEST_TIMEOUT = 10

logger = logging.getLogger(__name__)


########################################################################
class GitHubApiClient(object):
    """"""

    #----------------------------------------------------------------------
    def get_file_contents(self, filename):
        url_parameters = dict(user=GITHUB_USER,
                              repository=GITHUB_REPOSITORY,
                              filename=filename)
        url = 'https://api.github.com/repos/%(user)s/%(repository)s/contents/%(filename)s' % \
            url_parameters
        with requests.get(url, timeout=HTTP_REQUEST_TIMEOUT, stream=False) as response:
            response_json = response.json()
            self._log_rate_limit(response)

        # parse response
        return self._parse_fetch_file_response(response_json)

    #----------------------------------------------------------------------
    def _log_rate_limit(self, response):
        rate_limit_remaining = response.headers['X-RateLimit-Remaining']
        rate_limit = response.headers['X-RateLimit-Limit']
        logger.info('Github rate limits: %s/%s', rate_limit_remaining, rate_limit)

    #----------------------------------------------------------------------
    def _parse_fetch_file_response(self, response_json):
        if response_json['encoding'] == 'base64':
            # standard_b64decode returns a byte string but we want a unicode string
            content_utf8 = standard_b64decode(response_json['content'])
            return content_utf8.decode('utf-8')
        return content
