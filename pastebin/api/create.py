# coding: utf-8

from datetime import datetime, timedelta
from pastebin.forms import SnippetForm
from pastebin.highlight import LEXER_LIST_ALL, LEXER_DEFAULT
from pastebin.models import Snippet


# note: some mappings are equally but listing them anyways is more explicit
GEANY_LEXER_MAPPING = {
    'ActionScript': 'as',
    'Ada': 'ada',
    'C': 'c',
    'C++': 'cpp',
    'CAML': 'ocaml',
    'CMake': 'cmake',
    'CSS': 'css',
    'Conf': 'ini',
    'Cython': 'cython',
    'D': 'd',
    'Diff': 'diff',
    'Docbook': 'xml',
    'Erlang': 'erlang',
    'F77': 'fortran',
    'Fortran': 'fortran',
    'GLSL': 'glsl',
    'HTML': 'http',
    'Haskell': 'haskell',
    'Haxe': 'hx',
    'Java': 'java',
    'Javascript': 'js',
    'LaTeX': 'latex',
    'Lua': 'lua',
    'Make': 'make',
    'Matlab': 'matlab',
    'Objective-C': 'objective-c',
    'PHP': 'php',
    'Perl': 'perl',
    'Po': 'po',
    'Python': 'python',
    'R': 'rconsole',
    'reStructuredText': 'rst',
    'Ruby': 'ruby',
    'SQL': 'sql',
    'Scala': 'scala',
    'Sh': 'bash',
    'Tcl': 'tcl',
    'VHDL': 'vhdl',
    'Vala': 'vala',
    'Verilog': 'v',
    'XML': 'xml',
    'YAML': 'yaml',
}


########################################################################
class SnippetValidationError(Exception):
    pass


########################################################################
class CreateSnippetApiController(object):

    valid_fields = ('title', 'content', 'expires', 'author', 'lexer')

    #----------------------------------------------------------------------
    def __init__(self, request):
        self._request = request
        self._data = request.POST.copy()
        self._snippet = None
        self._snippet_form = None

    #----------------------------------------------------------------------
    def create(self):
        self._validate_passed_fields()
        self._validate_against_snippet_form()
        self._create_snippet()
        return self._snippet

    #----------------------------------------------------------------------
    def _validate_passed_fields(self):
        provided_fields = set(self._data.keys())
        additional_fields = provided_fields.difference(self.valid_fields)
        if additional_fields:
            raise SnippetValidationError(u'Invalid fields provided (%s)' % ','.join(additional_fields))

    #----------------------------------------------------------------------
    def _validate_against_snippet_form(self):
        self._preprocess_data()

        snippet_form = SnippetForm(request=self._request, data=self._data)
        # SnippetForm allows only a subset of lexer choices except the user enables all lexers
        # in her session but since we don't have a session here, we allow all unconditionally
        snippet_form.fields['lexer'].choices = LEXER_LIST_ALL
        # validate
        if not snippet_form.is_valid():
            errors = u'\n'.join([u'%s: %s' % (k, v.as_text()) for k, v in snippet_form.errors.items()])
            raise SnippetValidationError(errors)
        self._snippet_form = snippet_form

    #----------------------------------------------------------------------
    def _preprocess_data(self):
        # compatibility with SnippetForm
        self._data['expire_options'] = self._data.get('expires', 3600)
        # try to map lexer from a Geany filetype name to a Pygments lexer name
        # fallback to 'text' as default, also use that default in case no lexer was given at all
        try:
            original_lexer = self._data.get('lexer', LEXER_DEFAULT)
            self._data['lexer'] = GEANY_LEXER_MAPPING[original_lexer]
        except KeyError:
            if original_lexer in [lexer[0] for lexer in LEXER_LIST_ALL]:
                self._data['lexer'] = original_lexer
            else:
                # fall back to the text lexer as a last resort, this means we do accept invalid
                # lexers and simply override them with 'text'
                self._data['lexer'] = LEXER_DEFAULT

    #----------------------------------------------------------------------
    def _create_snippet(self):
        cleaned_data = self._snippet_form.cleaned_data
        expire_options = int(cleaned_data.get('expire_options', 3600))
        expires = datetime.now() + timedelta(seconds=expire_options)

        self._snippet = Snippet.objects.create(
            content=cleaned_data['content'],
            author=cleaned_data['author'],
            title=cleaned_data['title'],
            lexer=cleaned_data['lexer'],
            expires=expires)
        self._snippet.save()
