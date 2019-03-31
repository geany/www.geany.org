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

from django_hosts import host, patterns
from django_hosts.callbacks import cached_host_site


# ----------------------------------------------------------------------
def cached_host_site_extended(request, *args, **kwargs):
    # call the original django-hosts callback to do the work
    cached_host_site(request, *args, **kwargs)
    # now if it found a site, append its site.id to the request for Mezzanine
    if hasattr(request, 'site'):
        # TODO talk to Stephen about this
        request.site_id = request.site.id


host_patterns = patterns(
    '',
    # nightlybuilds (nightly.geany.org and nightly.local.geany.org)
    host(
        r'^nightly(\.local|\.dev)?\.geany\.org(:[0-9]*)?$', 'nightlybuilds.urls',
        name='nightly.geany.org',
        callback=cached_host_site_extended),
    host(
        r'^geany\.nightlybuilds\.org(:[0-9]*)?$', 'nightlybuilds.urls',
        name='geany.nightlybuilds.org',
        callback=cached_host_site_extended),

    # pastebin (pastebin.geany.org and pastebin.local.geany.org)
    host(
        r'^pastebin(\.local|\.dev)?\.geany\.org(:[0-9]*)?$', 'pastebin.urls',
        name='pastebin.geany.org',
        callback=cached_host_site_extended),

    # default
    host(
        r'^www\.geany\.org(:[0-9]*)?$', 'geany.urls',
        name='www.geany.org',
        callback=cached_host_site_extended),
)
