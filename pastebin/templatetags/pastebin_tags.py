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
from django.template.defaultfilters import timeuntil
from django.utils.timezone import now

from pastebin.highlight import pygmentize


NINETY_YEARS_IN_DAYS = 32850  # 90 * 365


register = Library()


# ----------------------------------------------------------------------
@register.filter
def timeuntil_or_forever(snippet_expire):
    ttl = snippet_expire - now()
    if ttl.days > NINETY_YEARS_IN_DAYS:
        # snippet TTL 'forever' is defined as 100 years, so if remaining TTL is more than
        # (90 * 365) days, we most probably got a snippet with TTL 'forever'
        return 'forever'

    return timeuntil(snippet_expire)


# ----------------------------------------------------------------------
@register.filter
def highlight(snippet, line_count=None):
    highlighted = pygmentize(snippet.content, snippet.lexer)
    if highlighted:
        lines = highlighted.splitlines()
    else:
        lines = snippet.content.splitlines()

    if line_count:
        lines = lines[:line_count]
        lines.append('...')
    return lines
