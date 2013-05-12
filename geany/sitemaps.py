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
