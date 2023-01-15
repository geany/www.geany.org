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
from django.views.decorators.cache import never_cache

from pastebin.views import (
    LatestSnippetsView,
    SnippetAPIView,
    SnippetDetailRawView,
    SnippetDetailView,
)


urlpatterns = (  # pylint: disable=invalid-name
    path('api/', never_cache(SnippetAPIView.as_view()), name='snippet_api'),

    path('', never_cache(LatestSnippetsView.as_view()), name='snippet_list'),
    path('latest/', never_cache(LatestSnippetsView.as_view()), name='snippet_list'),
    re_path(
        r'^(?P<snippet_id>[a-zA-Z0-9]+)/$',
        SnippetDetailView.as_view(),
        name='snippet_details'),
    re_path(
        r'^(?P<snippet_id>[a-zA-Z0-9]+)/raw/$',
        SnippetDetailRawView.as_view(),
        name='snippet_details_raw'),
)
