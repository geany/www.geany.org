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


urlpatterns = patterns('',
    # no admin on this site
    url(r'^admin/', 'mezzanine.core.views.page_not_found'),

    url(r'^about/$', TemplateView.as_view(template_name='pastebin/about.html'), name='about'),
    url(r'^about/api/$', TemplateView.as_view(template_name='pastebin/api.html'), name='api'),

    url(r'^api/$', 'pastebin.views.api_create'),

    url(r'^$', 'pastebin.views.snippet_new', name='home'),
    url(r'^latest/$', 'pastebin.views.snippet_list', name='snippet_list'),
    url(r'^(?P<snippet_id>[a-zA-Z0-9]+)/$', 'pastebin.views.snippet_details', name='snippet_details'),
    url(r'^(?P<snippet_id>[a-zA-Z0-9]+)/delete/$', 'pastebin.views.snippet_delete', name='snippet_delete'),
    url(r'^(?P<snippet_id>[a-zA-Z0-9]+)/raw/$', 'pastebin.views.snippet_details', {'template_name': 'pastebin/snippet_details_raw.html', 'is_raw': True}, name='snippet_details_raw'),
)

# Sitemap framework
sitemaps = {"sitemaps": {"all": StaticSitemap('pastebin.geany.org', urlpatterns)}}
urlpatterns += patterns('',
    # use our custom sitemap implementation
    url(r"^sitemap\.xml$", 'django.contrib.sitemaps.views.sitemap', sitemaps)
)
