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

from django.contrib.syndication.views import Feed
from django.urls import reverse
from mezzanine.conf import settings
from mezzanine.core.templatetags.mezzanine_tags import richtext_filters
from mezzanine.utils.html import absolute_urls

from news.models import NewsPost


class LatestNewsPostsFeed(Feed):

    title = "Geany project news"
    description = "News feed for the Geany project"

    # ----------------------------------------------------------------------
    def link(self):
        return reverse("news_list")

    # ----------------------------------------------------------------------
    def items(self):
        return NewsPost.objects.recently_published(count=200)

    # ----------------------------------------------------------------------
    def item_title(self, item):
        return item.title

    # ----------------------------------------------------------------------
    def item_description(self, item):
        description = richtext_filters(item.content)
        absolute_urls_name = "mezzanine.utils.html.absolute_urls"
        if absolute_urls_name not in settings.RICHTEXT_FILTERS:
            description = absolute_urls(description)
        return description

    # ----------------------------------------------------------------------
    def item_pubdate(self, item):
        return item.publish_date

    # ----------------------------------------------------------------------
    def item_author_name(self, item):
        return item.user.get_full_name() or item.user.username
