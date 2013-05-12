# -*- coding: utf-8 -*-

# try to get any json implementation
try:
    from django.utils import simplejson
except ImportError:
    try:
        import simplejson
    except ImportError:
        import json as simplejson
from base64 import standard_b64decode
import logging
import urllib2


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
        url = u'https://api.github.com/repos/%(user)s/%(repository)s/contents/%(filename)s' % \
            url_parameters
        handle = urllib2.urlopen(url, timeout=HTTP_REQUEST_TIMEOUT)
        self._log_rate_limit(handle)
        # parse response
        response_json = handle.read()
        return self._parse_fetch_file_response(response_json)

    #----------------------------------------------------------------------
    def _log_rate_limit(self, urllib_handle):
        headers = urllib_handle.info()
        rate_limit_remaining = headers['X-RateLimit-Remaining']
        rate_limit = headers['X-RateLimit-Limit']
        length = headers['Content-Length']
        logger.info(u'Github rate limits: %s/%s (%s bytes received)',
            rate_limit_remaining, rate_limit, length)

    #----------------------------------------------------------------------
    def _parse_fetch_file_response(self, response_json):
        response = simplejson.loads(response_json)
        content = response['content']
        if response[u'encoding'] == u'base64':
            # standard_b64decode returns a byte string but we want a unicode string
            content_utf8 = standard_b64decode(content)
            return content_utf8.decode('utf-8')
        return content
