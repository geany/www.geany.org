# coding: utf-8

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
