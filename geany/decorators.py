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
from django.core.cache import cache as _djcache
import inspect


CACHE_TIMEOUT_24HOURS = 3600 * 24
CACHE_TIMEOUT_1HOUR = 3600


#----------------------------------------------------------------------
def cache_function(timeout=900, ignore_arguments=False):
    """
        Cache the result of a function call for the specified number of seconds,
        using Django's caching mechanism.
        Assumes that the function never returns None (as the cache returns None to indicate a miss), and that the function's result only depends on its parameters.
        Note that the ordering of parameters is important. e.g. myFunction(x = 1, y = 2), myFunction(y = 2, x = 1), and myFunction(1,2) will each be cached separately.

        Usage:

        @cache(600)
        def myExpensiveMethod(parm1, parm2, parm3):
            ....
            return expensiveResult
    """
    def do_cache(f):
        def x(*args, **kwargs):
            key = '%s.%s' % ((f.__module__, f.__name__))
            if args and not ignore_arguments:
                cache_args = args
                # don't include 'self' in arguments
                arguments = inspect.getargspec(f)[0]
                if arguments and arguments[0] == 'self':
                    cache_args = args[1:]
                if cache_args:
                    key = '%s.args%s' % (key, hexlify(repr(cache_args)))
            if kwargs and not ignore_arguments:
                key = '%s.kwargs%s' % (key, hexlify(repr(kwargs)))
            result = _djcache.get(key)
            if result is None:
                result = f(*args, **kwargs)
                _djcache.set(key, result, timeout)
            return result
        return x
    return do_cache
