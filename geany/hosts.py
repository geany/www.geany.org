# -*- coding: utf-8 -*-

from django_hosts import patterns, host
from django_hosts.callbacks import cached_host_site


#----------------------------------------------------------------------
def cached_host_site_extended(request, *args, **kwargs):
    # call the original django-hosts callback to do the work
    cached_host_site(request, *args, **kwargs)
    # now if it found a site, append its site.id to the request for Mezzanine
    if hasattr(request, 'site'):
        # TODO talk to Stephen about this
        request.site_id = request.site.id


host_patterns = patterns('',
    # nightlybuilds (nightly.geany.org and nightly.local.geany.org)
    host(r'^nightly(\.local|\.dev)?\.geany\.org(:[0-9]*)?$', 'nightlybuilds.urls', name='nightly.geany.org', callback=cached_host_site_extended),
    host(r'^geany\.nightlybuilds\.org(:[0-9]*)?$', 'nightlybuilds.urls', name='geany.nightlybuilds.org', callback=cached_host_site_extended),

    # pastebin (pastebin.geany.org and pastebin.local.geany.org)
    host(r'^pastebin(\.local|\.dev)?\.geany\.org(:[0-9]*)?$', 'pastebin.urls', name='pastebin.geany.org', callback=cached_host_site_extended),

    # default
    host(r'^www\.geany\.org(:[0-9]*)?$', 'geany.urls', name='www.geany.org', callback=cached_host_site_extended),
)
