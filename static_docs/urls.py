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

from django.conf.urls import url
from static_docs.views import ReleaseNotesView, ToDoView


urlpatterns = (
    url(r'^documentation/todo/$', ToDoView.as_view(), name='todo'),

    url(r'^documentation/releasenotes/$', ReleaseNotesView.as_view(), name='releasenotes'),
    url(r'^documentation/releasenotes/(?P<version>.*)$', ReleaseNotesView.as_view(), name='releasenotes_for_release'),
)

# Adds ``STATIC_URL`` to the context of error pages, so that error pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
