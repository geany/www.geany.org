# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from pastebin.highlight import LEXER_LIST_ALL, LEXER_LIST, LEXER_DEFAULT
from pastebin.models import Snippet, Spamword
import datetime


#===============================================================================
# Snippet Form and Handling
#===============================================================================

EXPIRE_CHOICES = (
    (3600, _(u'In one hour')),
    (3600 * 24 * 7, _(u'In one week')),
    (3600 * 24 * 30, _(u'In one month')),
    (3600 * 24 * 30 * 12 * 100, _(u'Save forever')),  # 100 years, I call it forever ;)
)

EXPIRE_DEFAULT = 3600 * 24 * 30


########################################################################
class SnippetForm(forms.ModelForm):

    lexer = forms.ChoiceField(
        choices=LEXER_LIST,
        initial=LEXER_DEFAULT,
        label=_(u'Lexer'),
    )

    expire_options = forms.ChoiceField(
        choices=EXPIRE_CHOICES,
        initial=EXPIRE_DEFAULT,
        label=_(u'Expires'),
    )

    #----------------------------------------------------------------------
    def __init__(self, request, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.request = request

        try:
            if self.request.session['userprefs'].get('display_all_lexer', False):
                self.fields['lexer'].choices = LEXER_LIST_ALL
        except KeyError:
            pass

        try:
            self.fields['author'].initial = self.request.session['userprefs'].get('default_name', '')
        except KeyError:
            pass

    #----------------------------------------------------------------------
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content:
            regex = Spamword.objects.get_regex()
            if regex.findall(content.lower()):
                raise forms.ValidationError('This snippet was identified as SPAM.')
        return content

    #----------------------------------------------------------------------
    def save(self, parent=None, *args, **kwargs):

        # Set parent snippet
        if parent:
            self.instance.parent = parent

        # Add expire datestamp
        self.instance.expires = datetime.datetime.now() + \
            datetime.timedelta(seconds=int(self.cleaned_data['expire_options']))

        # Save snippet in the db
        forms.ModelForm.save(self, *args, **kwargs)

        return self.request, self.instance

    ########################################################################
    class Meta:
        model = Snippet
        fields = (
            'content',
            'title',
            'author',
            'lexer',)


########################################################################
class UserSettingsForm(forms.Form):

    default_name = forms.CharField(label=_(u'Default Name'), required=False)
    display_all_lexer = forms.BooleanField(
        label=_(u'Display all lexers'),
        required=False,
        widget=forms.CheckboxInput,
        help_text=_(u'This also enables the super secret \'guess lexer\' function.'),
    )
