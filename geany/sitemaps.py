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
from django.urls import NoReverseMatch, reverse
from mezzanine.conf import settings
from mezzanine.core.sitemaps import DisplayableSitemap


# Sitemap generation
# GeanyMainSitemap is the main class which generates sitemap items
# for all Mezzaine pages, blog posts, News posts and various static
# items.
#
# Other apps might add their own sitemap generator classes to the
# "sitemap_registry" provided by this module. For performance reasons,
# static sitemap items (i.e. items generated from URLconf patterns) are
# generated already on module-level because they never changed during
# the whole application lifetime.
# In addition, dynamic items (such as Pages and news posts) are added to
# the static items at runtime as they may change at any time.


class GeanyMainSitemap(DisplayableSitemap):
    """
    Sitemap class for Django's sitemaps framework that returns
    all published items for models that subclass ``Displayable``.
    """
    changefreq = 'monthly'
    priority = 0.5

    # ----------------------------------------------------------------------
    def items(self):
        items = super().items()
        additional_app_items = self._get_additional_app_items()
        items.extend(additional_app_items)
        return items

    # ----------------------------------------------------------------------
    def _get_additional_app_items(self):
        return sitemap_registry.get_all_items()

    # ----------------------------------------------------------------------
    def lastmod(self, obj):
        return getattr(obj, 'publish_date', None)


class SitemapItem:
    """Simulate a model, mainly to provide get_absolute_url() for Sitemaps"""

    # ----------------------------------------------------------------------
    def __init__(self, name, absolute_url, publish_date=None, priority=0.5):
        self._name = name
        self._absolute_url = absolute_url
        self._publish_date = publish_date
        self._priority = priority

    # ----------------------------------------------------------------------
    def get_absolute_url(self):
        return self._absolute_url

    # ----------------------------------------------------------------------
    @property
    def name(self):
        return self._name

    # ----------------------------------------------------------------------
    @property
    def publish_date(self):
        return self._publish_date

    # ----------------------------------------------------------------------
    @property
    def priority(self):
        return self._priority


class StaticSitemap(sitemaps.Sitemap):
    """Return the static sitemap items"""
    priority = 0.5

    # ----------------------------------------------------------------------
    def __init__(self, domain, patterns, exclude_views=None):
        self._domain = domain
        self._patterns = patterns
        self._exclude_views = exclude_views or []
        self._site = None
        self._url_mapping = {}
        self._get_site()

    # ----------------------------------------------------------------------
    def items(self):
        return self.get_static_items() + self.get_dynamic_items()

    # ----------------------------------------------------------------------
    def get_static_items(self):
        self._initialize()
        return [SitemapItem(name, url) for name, url in self._url_mapping.items()]

    # ----------------------------------------------------------------------
    def _initialize(self):
        for pattern in self._patterns:
            view_name = getattr(pattern, 'name', None)
            if view_name is not None and view_name not in self._exclude_views:
                url_resolved = self._resolve_url(pattern.name)
                if url_resolved:
                    self._url_mapping[pattern.name] = url_resolved

    # ----------------------------------------------------------------------
    def _get_site(self):
        self._site = Site.objects.get(domain=self._domain)

    # ----------------------------------------------------------------------
    def _resolve_url(self, url):
        try:
            return reverse(url)
        except NoReverseMatch:
            return None

    # ----------------------------------------------------------------------
    def get_dynamic_items(self):
        return []

    # ----------------------------------------------------------------------
    def changefreq(self, item):  # pylint: disable=unused-argument
        return 'monthly'

    # ----------------------------------------------------------------------
    def location(self, item):
        return self._url_mapping[item.name]

    # ----------------------------------------------------------------------
    def get_urls(self, page=1, site=None, protocol=None):
        # pass our site to the parent as we know better which site we are on
        return super().get_urls(page, self._site, protocol)


class SitemapRegistry:

    # ----------------------------------------------------------------------
    def __init__(self):
        self._sitemap_generators = []
        self._static_items = None
        self._site = None

    # ----------------------------------------------------------------------
    def add(self, generator_class, url_patterns, site_domain=None, exclude_views=None):
        sitemap_generator_item = (generator_class, url_patterns, site_domain, exclude_views)
        self._sitemap_generators.append(sitemap_generator_item)

    # ----------------------------------------------------------------------
    def _update_static_sitemap_items(self, sitemap_generator_class, url_patterns, site_domain):
        generator = sitemap_generator_class(site_domain, url_patterns)
        items = generator.get_static_items()
        self._static_items.extend(items)

    # ----------------------------------------------------------------------
    def get_all_items(self):
        if self._static_items is None:
            self._static_items = self._get_static_items()
        dynamic_items = self._get_dynamic_items()
        return self._static_items + dynamic_items

    # ----------------------------------------------------------------------
    def _get_static_items(self):
        return self._get_items('get_static_items')

    # ----------------------------------------------------------------------
    def _get_items(self, item_generator_name):
        items = []
        for generator_class, url_patterns, site_domain, exclude_views in self._sitemap_generators:
            site_domain = self._get_site_domain_or_default(site_domain)
            generator = generator_class(
                site_domain,
                url_patterns,
                exclude_views=exclude_views)
            item_generator = getattr(generator, item_generator_name)
            generated_items = item_generator()
            items.extend(generated_items)
        return items

    # ----------------------------------------------------------------------
    def _get_site_domain_or_default(self, site_domain):
        if site_domain is None:
            if self._site is None:
                self._site = Site.objects.get(id=settings.SITE_ID)

            site_domain = self._site.domain

        return site_domain

    # ----------------------------------------------------------------------
    def _get_dynamic_items(self):
        return self._get_items('get_dynamic_items')


sitemap_registry = SitemapRegistry()  # pylint: disable=invalid-name
