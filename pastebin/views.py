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

from datetime import datetime
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponseBadRequest, \
    HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from honeypot.decorators import check_honeypot
from pastebin.api.create import CreateSnippetApiController, SnippetValidationError
from pastebin.forms import SnippetForm, UserSettingsForm
from pastebin.highlight import pygmentize, guess_code_lexer
from pastebin.models import Snippet
import difflib


#----------------------------------------------------------------------
def _get_snippet_list(no_content=False):
    try:
        max_snippets = getattr(settings, 'MAX_SNIPPETS_PER_USER', 10)
        # TODO cache the result set and clear it upon Snippet.save()
        if no_content:
            queryset = Snippet.objects.defer('content', 'content_highlighted')
        else:
            queryset = Snippet.objects.all()

        snippet_list_ = queryset[:max_snippets]
    except ValueError:
        snippet_list_ = list()
    return snippet_list_


#----------------------------------------------------------------------
def _clean_expired_snippets():
    deleteable_snippets = Snippet.objects.filter(expires__lte=datetime.now())
    if deleteable_snippets:
        deleteable_snippets.delete()


#----------------------------------------------------------------------
@check_honeypot
def snippet_new(request, template_name='pastebin/snippet_new.html'):

    if request.method == "POST":
        snippet_form = SnippetForm(data=request.POST, request=request)
        if snippet_form.is_valid():
            request, new_snippet = snippet_form.save()
            return HttpResponseRedirect(new_snippet.get_absolute_url())
    else:
        # housekeeping
        _clean_expired_snippets()
        snippet_form = SnippetForm(request=request)

    snippet_list_ = _get_snippet_list(no_content=True)

    template_context = {
        'snippet_form': snippet_form,
        'snippet_list': snippet_list_,
    }

    return render_to_response(
        template_name,
        template_context,
        RequestContext(request)
    )


#----------------------------------------------------------------------
@check_honeypot
def snippet_details(request, snippet_id, template_name='pastebin/snippet_details.html', is_raw=False):

    # housekeeping
    _clean_expired_snippets()

    try:
        snippet = Snippet.objects.get(secret_id=snippet_id)
    except MultipleObjectsReturned:
        raise Http404('Multiple snippets exist for this slug. This should never '
                      'happen but its likely that you are a spam bot, so I dont '
                      'care.')
    except ObjectDoesNotExist:
        raise Http404('This snippet does not exist anymore. Its likely that its '
                      'lifetime is expired.')

    new_snippet_initial = {
        'content': snippet.content,
        'lexer': snippet.lexer,
    }

    if request.method == "POST":
        snippet_form = SnippetForm(data=request.POST, request=request, initial=new_snippet_initial)
        if snippet_form.is_valid():
            request, new_snippet = snippet_form.save(parent=snippet)
            return HttpResponseRedirect(new_snippet.get_absolute_url())
    else:
        snippet_form = SnippetForm(initial=new_snippet_initial, request=request)

    snippet_list_ = _get_snippet_list(no_content=True)
    template_context = {
        'snippet_list': snippet_list_,
        'snippet_form': snippet_form,
        'snippet': snippet,
        'lines': range(snippet.get_linecount()),
    }

    response = render_to_response(
        template_name,
        template_context,
        RequestContext(request)
    )

    if is_raw:
        response['Content-Type'] = 'text/plain;charset=UTF-8'
        return response
    else:
        return response


#----------------------------------------------------------------------
def snippet_delete(request, snippet_id):
    snippet = get_object_or_404(Snippet, secret_id=snippet_id)
    try:
        snippet_list_ = request.session['snippet_list']
    except KeyError:
        return HttpResponseForbidden('You have no recent snippet list, cookie error?')
    if not snippet.pk in snippet_list_:
        return HttpResponseForbidden('That\'s not your snippet, sucka!')
    snippet.delete()
    return HttpResponseRedirect(reverse('home'))


#----------------------------------------------------------------------
def snippet_list(request, template_name='pastebin/snippet_list.html'):

    snippet_list_ = _get_snippet_list()

    template_context = {
        'snippets_max': getattr(settings, 'MAX_SNIPPETS_PER_USER', 10),
        'snippet_list': snippet_list_,
    }

    return render_to_response(
        template_name,
        template_context,
        RequestContext(request)
    )


#----------------------------------------------------------------------
def userprefs(request, template_name='pastebin/userprefs.html'):

    if request.method == 'POST':
        settings_form = UserSettingsForm(request.POST, initial=request.session.get('userprefs', None))
        if settings_form.is_valid():
            request.session['userprefs'] = settings_form.cleaned_data
            settings_saved = True
    else:
        settings_form = UserSettingsForm(initial=request.session.get('userprefs', None))
        settings_saved = False

    template_context = {
        'settings_form': settings_form,
        'settings_saved': settings_saved,
    }

    return render_to_response(
        template_name,
        template_context,
        RequestContext(request))


#----------------------------------------------------------------------
def snippet_diff(request, template_name='pastebin/snippet_diff.html'):

    if request.GET.get('a') and request.GET.get('a').isdigit() \
                    and request.GET.get('b') and request.GET.get('b').isdigit():
        try:
            fileA = Snippet.objects.get(pk=int(request.GET.get('a')))
            fileB = Snippet.objects.get(pk=int(request.GET.get('b')))
        except ObjectDoesNotExist:
            return HttpResponseBadRequest(u'Selected file(s) does not exist.')
    else:
        return HttpResponseBadRequest(u'You must select two snippets.')

    if fileA.content != fileB.content:
        d = difflib.unified_diff(
            fileA.content.splitlines(),
            fileB.content.splitlines(),
            'Original',
            'Current',
            lineterm=''
        )
        difftext = '\n'.join(d)
        difftext = pygmentize(difftext, 'diff')
    else:
        difftext = _(u'No changes were made between this two files.')

    template_context = {
        'difftext': difftext,
        'fileA': fileA,
        'fileB': fileB,
    }

    return render_to_response(
        template_name,
        template_context,
        RequestContext(request))


#----------------------------------------------------------------------
def guess_lexer(request):
    code_string = request.GET.get('codestring', False)
    response = simplejson.dumps({'lexer': guess_code_lexer(code_string)})
    return HttpResponse(response)


#----------------------------------------------------------------------
def _get_site(request):
    if hasattr(request, 'site'):
        return request.site
    else:
        return Site.objects.get_current()


#----------------------------------------------------------------------
@require_POST
@csrf_exempt
def api_create(request):
    """
    View for snippet creation via API
    """
    try:
        controller = CreateSnippetApiController(request)
        snippet = controller.create()
    except SnippetValidationError, e:
        return HttpResponseBadRequest(unicode(e), content_type=u'text/plain')

    site = _get_site(request)
    absolute_url = snippet.get_absolute_url()
    result = u'http://%s%s/' % (site.domain, absolute_url)
    return HttpResponse(result, content_type=u'text/plain')
