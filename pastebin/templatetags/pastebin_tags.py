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

from django.template import Library
from pastebin.highlight import pygmentize


register = Library()


#----------------------------------------------------------------------
@register.filter
def in_list(value, arg):
    return value in arg


#----------------------------------------------------------------------
@register.filter
def highlight(snippet, line_count=None):
    h = pygmentize(snippet.content, snippet.lexer)
    if h:
        lines = h.splitlines()
    else:
        lines = snippet.content.splitlines()

    if line_count:
        lines = lines[:line_count]
        lines.append(u'...')
    return lines
