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

from django.urls import path, re_path

from news.feeds import LatestNewsPostsFeed
from news.views import NewsDetailView, NewsListView


urlpatterns = (  # pylint: disable=invalid-name
    path('', NewsListView.as_view(), name='news_list'),
    path('feed/', LatestNewsPostsFeed(), name='news_feed'),
    re_path(r'^(?P<newspost_slug>.+)/$', NewsDetailView.as_view(), name='news_detail'),
)
