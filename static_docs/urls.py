# coding: utf-8

from django.conf.urls import patterns, url
from static_docs.views import ReleaseNotesView, ToDoView


urlpatterns = patterns('',
    url(r'^documentation/todo/$', ToDoView.as_view(), name='todo'),

    url(r'^documentation/releasenotes/$', ReleaseNotesView.as_view(), name='releasenotes'),
    url(r'^documentation/releasenotes/(?P<version>.*)$', ReleaseNotesView.as_view(), name='releasenotes_for_release'),
)
