# coding: utf-8

from django.conf.urls import url, patterns, include
from django.views.generic.base import TemplateView


urlpatterns = patterns('',
    # no admin on this site
    url(r'^admin/', 'mezzanine.core.views.page_not_found'),

    url(r'^about/$', TemplateView.as_view(template_name='pastebin/about.html'), name='about'),
    url(r'^about/api/$', TemplateView.as_view(template_name='pastebin/api.html'), name='api'),

    url(r'^api/$', 'pastebin.views.api_create'),

    url(r'^$', 'pastebin.views.snippet_new', name='home'),
    url(r'^guess/$', 'pastebin.views.guess_lexer', name='snippet_guess_lexer'),
    url(r'^latest/$', 'pastebin.views.snippet_list', name='snippet_list'),
    url(r'^your-settings/$', 'pastebin.views.userprefs', name='snippet_userprefs'),
    url(r'^(?P<snippet_id>[a-zA-Z0-9]+)/$', 'pastebin.views.snippet_details', name='snippet_details'),
    url(r'^(?P<snippet_id>[a-zA-Z0-9]+)/delete/$', 'pastebin.views.snippet_delete', name='snippet_delete'),
    url(r'^(?P<snippet_id>[a-zA-Z0-9]+)/raw/$', 'pastebin.views.snippet_details', {'template_name': 'pastebin/snippet_details_raw.html', 'is_raw': True}, name='snippet_details_raw'),
)
