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

from django import template

from news.models import NewsPost


register = template.Library()


# ----------------------------------------------------------------------
@register.inclusion_tag("news/list_embedded.html", takes_context=True)
def get_recent_news(context):
    user = context.request.user
    context["recent_news_posts"] = NewsPost.objects.recently_published(count=4, for_user=user)
    return context
