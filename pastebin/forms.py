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

from django import forms
from django.utils.translation import gettext_lazy as _

from pastebin.highlight import LEXER_DEFAULT, LEXER_LIST
from pastebin.models import Snippet, Spamword


# ===============================================================================
# Snippet Form and Handling
# ===============================================================================

EXPIRE_CHOICES = (
    (3600, _('In one hour')),
    (3600 * 24 * 7, _('In one week')),
    (3600 * 24 * 30, _('In one month')),
    (3600 * 24 * 30 * 12 * 100, _('Save forever')),  # 100 years, I call it forever ;)
)

EXPIRE_DEFAULT = 3600 * 24 * 30


class SnippetForm(forms.ModelForm):

    lexer = forms.ChoiceField(
        choices=LEXER_LIST,
        initial=LEXER_DEFAULT,
        label=_('Lexer'),
    )

    expire_options = forms.ChoiceField(
        choices=EXPIRE_CHOICES,
        initial=EXPIRE_DEFAULT,
        label=_('Expires'),
    )

    class Meta:
        model = Snippet
        fields = (
            'content',
            'title',
            'author',
            'lexer',)

    # ----------------------------------------------------------------------
    def _clean_field(self, field_name):
        value = self.cleaned_data.get(field_name)
        if value:
            regex = Spamword.objects.get_regex()
            if regex.findall(value.lower()):
                raise forms.ValidationError('This snippet was identified as SPAM.')

        return value

    # ----------------------------------------------------------------------
    def clean_author(self):
        return self._clean_field('author')

    # ----------------------------------------------------------------------
    def clean_content(self):
        return self._clean_field('content')

    # ----------------------------------------------------------------------
    def clean_title(self):
        return self._clean_field('title')
