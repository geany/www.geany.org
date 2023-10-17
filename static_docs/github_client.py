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

from base64 import standard_b64decode, standard_b64encode
import logging

import requests


GITHUB_API_URL = 'https://api.github.com/'
GITHUB_USER = 'geany'
GITHUB_REPOSITORY = 'geany'
HTTP_REQUEST_TIMEOUT = 10

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class GitHubApiClient:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, auth_token=None):
        self._auth_token = auth_token

    # ----------------------------------------------------------------------
    def get_file_contents(self, filename, user=None, repository=None):
        user = user or GITHUB_USER
        repository = repository or GITHUB_REPOSITORY
        url = f'{GITHUB_API_URL}repos/{user}/{repository}/contents/{filename}'
        response = self._request(url)
        response_json = response.json()

        # parse response
        return self._parse_fetch_file_response(response_json)

    # ----------------------------------------------------------------------
    def _request(self, url, status_404_expected=False):
        request_args = {'timeout': HTTP_REQUEST_TIMEOUT, 'stream': False}
        if self._auth_token is not None:
            authorization_header = self._factor_authorization_header()
            request_args['headers'] = authorization_header

        try:
            with requests.get(url, **request_args) as response:
                self._log_request(response, status_404_expected)
                self._log_rate_limit(response)
                # error out on 4xx and 5xx status codes
                response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            if exc.response.status_code == 404 and status_404_expected:
                return None
            else:
                raise

        return response

    # ----------------------------------------------------------------------
    def _factor_authorization_header(self):
        auth = f'{self._auth_token}:x-oauth-basic'
        auth_encoded = auth.encode('ascii')
        auth_base64 = standard_b64encode(auth_encoded).decode()
        basic_auth_value = f'Basic {auth_base64}'
        return {'Authorization': basic_auth_value}

    # ----------------------------------------------------------------------
    def _log_rate_limit(self, response):
        rate_limit_remaining = response.headers.get('X-RateLimit-Remaining')
        if rate_limit_remaining:
            rate_limit_remaining = int(rate_limit_remaining)
            rate_limit = response.headers['X-RateLimit-Limit']
            log_message = f'Github rate limits: {rate_limit_remaining}/{rate_limit}'
            if rate_limit_remaining > 0:
                logger.info(log_message)
            else:
                logger.warning(log_message)

    # ----------------------------------------------------------------------
    def _log_request(self, response, status_404_expected):
        # try to parse response as JSON (if it is a API error) and set the message
        # as reason or just use the plain text from the response
        if response.status_code >= 400:
            try:
                response_json = response.json()
                reason = response_json.get('message')
            except ValueError:
                reason = response.text
        else:
            reason = response.reason

        log_message = 'Requesting "%s %s" took %0.3fs: %s (%s)'
        log_message_args = (
            response.request.method,
            response.request.url,
            response.elapsed.total_seconds(),
            response.status_code,
            reason)

        if response.status_code == 200:
            logger.info(log_message, *log_message_args)
        elif response.status_code == 404 and status_404_expected:
            logger.info(log_message, *log_message_args)
        else:
            logger.warning(log_message, *log_message_args)

    # ----------------------------------------------------------------------
    def _parse_fetch_file_response(self, response_json):
        content = response_json['content']
        if response_json['encoding'] == 'base64':
            # standard_b64decode returns a byte string but we want a unicode string
            content_utf8 = standard_b64decode(content)
            return content_utf8.decode('utf-8')
        elif response_json['encoding'] == 'none' and not content:
            # the API did not return the file content, so download it explicitly
            file_content = self._request(response_json['download_url'])
            return file_content.text

        return content

    # ----------------------------------------------------------------------
    def get_release_by_tag(self, tag_name):
        url = f'{GITHUB_API_URL}repos/{GITHUB_USER}/{GITHUB_REPOSITORY}/releases/tags/{tag_name}'
        response = self._request(url, status_404_expected=True)
        if response:
            response_json = response.json()
            return response_json

        return None

    # ----------------------------------------------------------------------
    def get_latest_release(self):
        url = f'{GITHUB_API_URL}repos/{GITHUB_USER}/{GITHUB_REPOSITORY}/releases/latest'
        response = self._request(url)
        response_json = response.json()
        return response_json
