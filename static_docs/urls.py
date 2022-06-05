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

from django.urls import path

from static_docs.views import I18NStatisticsView, ReleaseNotesView, ThemesView, ToDoView


urlpatterns = (  # pylint: disable=invalid-name
    path('download/themes/', ThemesView.as_view(), name='themes'),

    path('documentation/todo/', ToDoView.as_view(), name='todo'),

    path('documentation/releasenotes/', ReleaseNotesView.as_view(), name='releasenotes'),
    path(
        'documentation/releasenotes/<version>/',
        ReleaseNotesView.as_view(),
        name='releasenotes_for_release'),

    path(
        'contribute/translation/statistics/',
        I18NStatisticsView.as_view(),
        name='translation_statistics'),
)
