# -*- coding: utf-8 -*-

from latest_version.models import LatestVersion
from geany.decorators import cache_function, CACHE_TIMEOUT_1HOUR


#----------------------------------------------------------------------
@cache_function(CACHE_TIMEOUT_1HOUR, ignore_arguments=True)
def latest_version(request):
    geany_latest_version = LatestVersion.objects.get(id=1)
    return dict(geany_latest_version=geany_latest_version)
