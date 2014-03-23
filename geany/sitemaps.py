# coding: utf-8
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

from django.contrib import sitemaps
from django.contrib.sites.models import Site
from django.core import urlresolvers
from django_hosts.resolvers import get_host
from mezzanine.blog.models import BlogPost
from mezzanine.core.sitemaps import DisplayableSitemap


########################################################################
class GeanyDisplayableSitemap(DisplayableSitemap):
    """
    Sitemap class for Django's sitemaps framework that returns
    all published items for models that subclass ``Displayable``.
    """
    changefreq = 'monthly'

    #----------------------------------------------------------------------
    def lastmod(self, obj):
        return obj.publish_date

    #----------------------------------------------------------------------
    def priority(self, obj):
        if isinstance(obj, BlogPost):
            return 1
        else:
            return 0.5


########################################################################
class StaticSitemap(sitemaps.Sitemap):
    """Return the static sitemap items"""
    priority = 0.5

    #----------------------------------------------------------------------
    def __init__(self, domain, patterns):
        self._domain = domain
        self._patterns = patterns
        self._site = None
        self._host = None
        self._items = {}
        self._get_site_and_host()
        self._initialize()

    #----------------------------------------------------------------------
    def _get_site_and_host(self):
        self._site = Site.objects.get(domain=self._domain)
        self._host = get_host(self._domain)

    #----------------------------------------------------------------------
    def _initialize(self):
        for pattern in self._patterns:
            if getattr(pattern, 'name', None) is not None:
                url_resolved = self._resolve_url(pattern.name)
                if url_resolved:
                    self._items[pattern.name] = url_resolved

    #----------------------------------------------------------------------
    def _resolve_url(self, url):
        try:
            return urlresolvers.reverse(url, urlconf=self._host.urlconf)
        except urlresolvers.NoReverseMatch:
            return None

    #----------------------------------------------------------------------
    def items(self):
        return self._items.keys()

    #----------------------------------------------------------------------
    def changefreq(self, obj):
        return 'monthly'

    #----------------------------------------------------------------------
    def location(self, obj):
        return self._items[obj]

    #----------------------------------------------------------------------
    def get_urls(self, page=1, site=None, protocol=None):
        # pass our site to the parent as we know better which site we are on
        return super(StaticSitemap, self).get_urls(page, self._site, protocol)
