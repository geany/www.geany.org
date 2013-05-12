# -*- coding: utf-8 -*-
# based on http://djangosnippets.org/snippets/564/

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
