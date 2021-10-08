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

from django.contrib import admin
from mezzanine.core.models import CONTENT_STATUS_DRAFT, CONTENT_STATUS_PUBLISHED

from news.models import NewsPost


class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'publish_date')
    list_editable = ("status",)
    list_filter = ('publish_date', 'status')
    date_hierarchy = 'publish_date'
    exclude = ('slug', 'user', 'entry_date')
    actions = ['_toggle_many_published']
    radio_fields = {"status": admin.HORIZONTAL}

    # ----------------------------------------------------------------------
    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            # set logged in user as author
            obj.user = request.user
        obj.save()

    # ----------------------------------------------------------------------
    def _toggle_many_published(self, request, queryset):
        # this is not really as efficient as it could be as the query is performed, but I don't know
        # a way to get the primary keys in the queryset without executing it
        rows_updated = 0
        for newspost in queryset:
            self._toggle_newspost_published_status(newspost)
            rows_updated += 1
        self.message_user(request, f'{rows_updated} News posts were successfully changed.')

    # ----------------------------------------------------------------------
    def _toggle_newspost_published_status(self, newspost):
        if newspost.status == CONTENT_STATUS_PUBLISHED:
            newspost.status = CONTENT_STATUS_DRAFT
        else:
            newspost.status = CONTENT_STATUS_PUBLISHED
        newspost.save()

    _toggle_many_published.short_description = 'Toggle the published status of selected News posts'


admin.site.register(NewsPost, NewsPostAdmin)
