# coding: utf-8

from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    # compat / special url for the UpdateChecker Geany plugin
    url(r'^service/version.php', TemplateView.as_view(
                                    template_name='latest_version.txt',
                                    content_type='text/plain'),
                            name='latest_version'),
)
