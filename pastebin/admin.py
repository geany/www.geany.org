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
from django.template.defaultfilters import truncatewords

from pastebin.models import Snippet, Spamword


class SnippetAdmin(admin.ModelAdmin):
    list_display = ('published', 'author', 'title', 'get_content_preview')
    date_hierarchy = 'published'
    list_filter = ('published', 'lexer')

    def get_content_preview(self, obj):
        return truncatewords(obj.content, 15)

    get_content_preview.allow_tags = True
    get_content_preview.short_description = 'Content'


admin.site.register(Snippet, SnippetAdmin)
admin.site.register(Spamword)
