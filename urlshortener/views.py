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

import json
import logging

from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic.base import View
from shortener import shortener


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(require_POST, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class UrlShortenerAPIView(View):
    """
    Provide a simple create API view for URL shortener app:
    - JSON API
    - requires Basic Auth
    - Input:
        {
            "auth": {
                "username": "username",
                "password": "secret",
            },
            "url": {
                "fullUrl": "https://..."}
            }
        }
    - Output:
        {
            "statusCode": 200,
            "errorMessage": "...",
            "url": {
                "fullUrl": "https://...",
                "shortUrl": "https://geany.org/s/ABCDEFG/"
            }
        }
    """

    # ----------------------------------------------------------------------
    def post(self, request):
        try:
            request_data = self._parse_request()
            self._validate_request_data(request_data)
        except Exception as exc:
            logger.info('Invalid short url API request: {}'.format(exc))
            response_body = dict(errorMessage='Invalid JSON: {}'.format(exc), statusCode=400)
            return JsonResponse(response_body, status=400)

        # authenticate user
        try:
            user = self._authenticate_request(request_data)
        except Exception as exc:
            # log the exception text but do not pass it to the response
            logger.info('Unauthorized short url API request: {}'.format(exc))
            response_body = dict(
                errorMessage='Unauthorized: Invalid username or password',
                statusCode=401)
            return JsonResponse(response_body, status=401)

        full_url = request_data['url']['fullUrl']
        short_url_code = shortener.create(user, full_url)

        short_url = reverse('url_shortener_expand', args=(short_url_code,))
        absolute_short_url = request.build_absolute_uri(short_url)

        logger.debug(
            'Created short URL "{}" for full URL "{}" (user "{}")'.format(
                absolute_short_url,
                full_url,
                user.username))
        response_body = dict(
            statusCode=200,
            url=dict(
                fullUrl=full_url,
                shortUrl=absolute_short_url))
        return JsonResponse(response_body)

    # ----------------------------------------------------------------------
    def _get_user(self, request_data):
        username = request_data['auth']['username']

    # ----------------------------------------------------------------------
    def _parse_request(self):
        request_body = self.request.body
        request_data = request_body.decode('utf-8')
        return json.loads(request_data)

    # ----------------------------------------------------------------------
    def _validate_request_data(self, request_data):
        self._validate_request_data_field(request_data, 'auth')
        self._validate_request_data_field(request_data, 'auth.username')
        self._validate_request_data_field(request_data, 'auth.password')
        self._validate_request_data_field(request_data, 'url')
        self._validate_request_data_field(request_data, 'url.fullUrl')

        validator = URLValidator(schemes=('http', 'https'))
        validator(request_data['url']['fullUrl'])

    # ----------------------------------------------------------------------
    def _validate_request_data_field(self, request_data, field_name):
        field_parts = field_name.split('.')
        element = request_data
        for field_part in field_parts:
            element = element.get(field_part, None)
            if not element:  # check for None and empty strings on purpose as both are failures
                raise ValueError('Missing element "{}"'.format(field_name))

    # ----------------------------------------------------------------------
    def _authenticate_request(self, request_data):
        username = request_data['auth']['username']
        password = request_data['auth']['password']
        # lookup user (throws exception if user does not exist)
        user = User.objects.get(username=username)
        # check password
        if user.check_password(password):
            return user
        else:
            raise ValueError('Invalid password')
