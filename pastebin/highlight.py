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
from pygments.formatters import HtmlFormatter
from pygments import highlight
from pygments.lexers import (
    PythonLexer,
    get_all_lexers,
    get_lexer_by_name)


LEXER_LIST_ALL = sorted([(i[1][0], i[0]) for i in get_all_lexers()])
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


########################################################################
class NakedHtmlFormatter(HtmlFormatter):

    #----------------------------------------------------------------------
    def wrap(self, source, outfile):
        return self._wrap_code(source)

    #----------------------------------------------------------------------
    def _wrap_code(self, source):
        for j, t in source:
            yield j, t


#----------------------------------------------------------------------
def pygmentize(code_string, lexer_name=LEXER_DEFAULT):
    try:
        if lexer_name:
            lexer = get_lexer_by_name(lexer_name)
        else:
            raise Exception(u'Unknown lexer')
    except:
        lexer = PythonLexer()

    try:
        return highlight(code_string, lexer, NakedHtmlFormatter())
    except:
        return escape(code_string)
