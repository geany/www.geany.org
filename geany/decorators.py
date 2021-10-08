# -*- coding: utf-8 -*-
# based on http://djangosnippets.org/snippets/564/
#
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

from binascii import hexlify
import inspect

from django.core.cache import cache as _djcache


CACHE_TIMEOUT_24HOURS = 3600 * 24
CACHE_TIMEOUT_1HOUR = 3600

CACHE_KEY_LATEST_VERSION_LATEST_VERSION = 'latest_version.latest_version'
CACHE_KEY_STATIC_DOCS_RELEASE_NOTES = 'static_docs.release_notes'


# ----------------------------------------------------------------------
def cache_function(timeout=900, ignore_arguments=False, key=None):
    """
        Cache the result of a function call for the specified number of seconds,
        using Django's caching mechanism.
        Assumes that the function never returns None (as the cache returns None to indicate a miss),
        and that the function's result only depends on its parameters.
        Note that the ordering of parameters is important. e.g.
        myFunction(x = 1, y = 2), myFunction(y = 2, x = 1), and myFunction(1,2)
        will each be cached separately.

        If the keyword argument `key` is provided, automatic cache key generation is skipped
        and the passed key is used instead (expected as string).

        Usage:

        @cache(600)
        def myExpensiveMethod(parm1, parm2, parm3):
            ....
            return expensiveResult
    """
    def do_cache(function):
        def wrapped(*args, **kwargs):
            cache_key = key
            if cache_key is None:
                cache_key = f'{function.__module__}.{function.__name__}'
                if args and not ignore_arguments:
                    cache_args = args
                    # don't include 'self' in arguments
                    arguments = inspect.getfullargspec(function)
                    if arguments and arguments.args[0] == 'self':
                        cache_args = args[1:]
                    if cache_args:
                        cache_args_repr = repr(cache_args).encode('utf-8')
                        cache_key = f'{cache_key}.args{hexlify(cache_args_repr)}'
                if kwargs and not ignore_arguments:
                    kwargs_repr = repr(kwargs).encode('utf-8')
                    cache_key = f'{cache_key}.kwargs{hexlify(kwargs_repr)}'
            result = _djcache.get(cache_key)
            if result is None:
                result = function(*args, **kwargs)
                _djcache.set(cache_key, result, timeout)
            return result
        return wrapped
    return do_cache
