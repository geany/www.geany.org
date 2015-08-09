# -*- coding: utf-8 -*-
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

from django.conf.urls import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.templatetags.static import static
from mezzanine.core.models import CONTENT_STATUS_DRAFT, CONTENT_STATUS_PUBLISHED
from news.models import NewsPost


########################################################################
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', '_is_published_switch', 'publish_date')
    date_hierarchy = 'publish_date'
    list_filter = ('publish_date', 'status')
    exclude = ('slug', 'user', 'entry_date')
    actions = ['_toggle_many_published']

    #----------------------------------------------------------------------
    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            # set logged in user as author
            obj.user = request.user
        obj.save()

    #----------------------------------------------------------------------
    def get_urls(self):
        urls = admin.ModelAdmin.get_urls(self)
        my_urls = patterns(
            '',
            url(
                r'^toggle_published/([0-9]+)/$',
                self.admin_site.admin_view(self._toggle_published),
                name='news_post_toggle_published'),)
        return my_urls + urls

    #----------------------------------------------------------------------
    def _is_published_switch(self, obj):
        toggle_published_url = reverse('admin:news_post_toggle_published', args=(obj.id,))
        yes_no = 'yes' if obj.status == CONTENT_STATUS_PUBLISHED else 'no'
        static_path = static('admin/img/icon-{}.gif'.format(yes_no))
        value = obj.status
        return '<a href="{}"><img src="{}" alt="{}"/></a>'.format(
            toggle_published_url,
            static_path,
            value)

    #----------------------------------------------------------------------
    def _toggle_published(self, request, newspost_id):
        newspost = NewsPost.objects.get(pk=newspost_id)
        self._toggle_newspost_published_status(newspost)
        self.message_user(
            request,
            u'News post public status have been changed.',
            fail_silently=True)
        # redirect back to the changelist page
        changelist_url = self._admin_url('changelist')
        return HttpResponseRedirect(changelist_url)

    #----------------------------------------------------------------------
    def _toggle_newspost_published_status(self, newspost):
        if newspost.status == CONTENT_STATUS_PUBLISHED:
            newspost.status = CONTENT_STATUS_DRAFT
        else:
            newspost.status = CONTENT_STATUS_PUBLISHED
        newspost.save()

    #----------------------------------------------------------------------
    def _admin_url(self, target_url):
        opts = self.model._meta
        url_ = "admin:%s_%s_%s" % (opts.app_label, opts.object_name.lower(), target_url)
        return reverse(url_)

    #----------------------------------------------------------------------
    def _toggle_many_published(self, request, queryset):
        # this is not really as efficient as it could be as the query is performed, but I don't know
        # a way to get the primary keys in the queryset without executing it
        rows_updated = 0
        for newspost in queryset:
            self._toggle_newspost_published_status(newspost)
            rows_updated += 1
        self.message_user(request, "{} News posts were successfully changed.".format(rows_updated))

    _is_published_switch.allow_tags = True
    _is_published_switch.short_description = 'Is published'
    _toggle_many_published.short_description = "Toggle the published status of selected News posts"


admin.site.register(NewsPost, NewsPostAdmin)
