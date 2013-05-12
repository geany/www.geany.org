# coding: utf-8

from django.conf.urls import url, patterns
from nightlybuilds.views import NightlyBuildsView


urlpatterns = patterns('',
    # no admin on this site
    url(r'^admin/', 'mezzanine.core.views.page_not_found'),

    url(r'^$', NightlyBuildsView.as_view(), name='home'),
)
