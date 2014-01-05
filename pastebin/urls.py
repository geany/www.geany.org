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


from django.conf.urls import url, patterns
from django.views.generic.base import TemplateView
from geany.sitemaps import StaticSitemap
from pastebin.views import (
    LatestSnippetsView,
    SnippetAPIView,
    SnippetDeleteView,
    SnippetDetailRawView,
    SnippetDetailView,
    SnippetNewView)


urlpatterns = patterns('',
    # no admin on this site
    url(r'^admin/', 'mezzanine.core.views.page_not_found'),

    url(r'^help/$', TemplateView.as_view(template_name='pastebin/help.html'), name='help'),
    url(r'^help/api/$', TemplateView.as_view(template_name='pastebin/api.html'), name='api'),

    url(r'^api/$', SnippetAPIView.as_view()),

    url(r'^$', SnippetNewView.as_view(), name='home'),
    url(r'^latest/$', LatestSnippetsView.as_view(), name='snippet_list'),
    url(r'^(?P<snippet_id>[a-zA-Z0-9]+)/$', SnippetDetailView.as_view(), name='snippet_details'),
    url(r'^(?P<snippet_id>[a-zA-Z0-9]+)/delete/$', SnippetDeleteView.as_view(), name='snippet_delete'),
    url(r'^(?P<snippet_id>[a-zA-Z0-9]+)/raw/$', SnippetDetailRawView.as_view(), name='snippet_details_raw'),
)

# Sitemap framework
sitemaps = {"sitemaps": {"all": StaticSitemap('pastebin.geany.org', urlpatterns)}}
urlpatterns += patterns('',
    # use our custom sitemap implementation
    url(r"^sitemap\.xml$", 'django.contrib.sitemaps.views.sitemap', sitemaps)
)
