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

from django.utils.html import escape
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.lexers.python import PythonLexer


LEXER_LIST_ALL = sorted([
    (lexer[1][0], lexer[0])
    for lexer in get_all_lexers()
    if lexer[1]])
LEXER_LIST = (
    ('nasm', 'Assembler'),
    ('bash', 'Bash'),
    ('c', 'C'),
    ('cpp', 'C++'),
    ('css', 'CSS'),
    ('diff', 'Diff'),
    ('django', 'Django/Jinja'),
    ('po', 'Gettext/Po'),
    ('html', 'HTML'),
    ('ini', 'INI config file'),
    ('irc', 'IRC logs'),
    ('java', 'Java'),
    ('js', 'JavaScript'),
    ('json', 'JSON'),
    ('lua', 'Lua'),
    ('perl', 'Perl'),
    ('php', 'PHP'),
    ('python', 'Python'),
    ('rst', 'Restructured Text'),
    ('ruby', 'Ruby'),
    ('sql', 'SQL'),
    ('text', 'Text only'),
    ('vala', 'Vala'),
    ('xml', 'XML'),
)
LEXER_DEFAULT = 'text'


class NakedHtmlFormatter(HtmlFormatter):
    """Do not wrap the code in <div> or <code> tags (Pygments default)"""

    # ----------------------------------------------------------------------
    def wrap(self, source):
        return self._wrap_code(source)

    # ----------------------------------------------------------------------
    def _wrap_code(self, inner):
        yield from inner

    # ----------------------------------------------------------------------
    def _wrap_div(self, inner):
        yield from inner


# ----------------------------------------------------------------------
def pygmentize(code_string, lexer_name=LEXER_DEFAULT):
    try:
        if lexer_name:
            lexer = get_lexer_by_name(lexer_name)
        else:
            raise Exception('Unknown lexer')
    except Exception:
        lexer = PythonLexer()

    try:
        return highlight(code_string, lexer, NakedHtmlFormatter())
    except Exception:
        return escape(code_string)
