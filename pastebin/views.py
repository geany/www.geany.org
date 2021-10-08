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

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, View
from honeypot.decorators import check_honeypot

from geany.decorators import CACHE_TIMEOUT_24HOURS
from pastebin.api.create import CreateSnippetApiController, SnippetValidationError
from pastebin.forms import SnippetForm
from pastebin.models import CACHE_KEY_SNIPPET_LIST_FULL, CACHE_KEY_SNIPPET_LIST_NO_CONTENT, Snippet


# ----------------------------------------------------------------------
def _get_snippet_list(no_content=False):
    if no_content:
        queryset = Snippet.objects.defer('content', 'content_highlighted')
        cache_key = CACHE_KEY_SNIPPET_LIST_NO_CONTENT
    else:
        queryset = Snippet.objects.all()
        cache_key = CACHE_KEY_SNIPPET_LIST_FULL

    # snippet list in cache?
    snippet_list = cache.get(cache_key, None)
    if snippet_list is not None:
        return snippet_list

    # nothing in cache, fetch snippets from the database
    try:
        max_snippets = getattr(settings, 'MAX_SNIPPETS_PER_USER', 10)
        snippet_list = list(queryset[:max_snippets])
        cache.set(cache_key, snippet_list, CACHE_TIMEOUT_24HOURS)
    except ValueError:
        snippet_list = []
    return snippet_list


class SnippetNewView(View):
    template_name = 'pastebin/snippet_new.html'

    # ----------------------------------------------------------------------
    @method_decorator(check_honeypot)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # ----------------------------------------------------------------------
    def get(self, request):
        snippet_form = SnippetForm(request=request)
        return self._render_response(request, snippet_form)

    # ----------------------------------------------------------------------
    def _render_response(self, request, snippet_form):
        snippet_list = _get_snippet_list(no_content=True)
        template_context = dict(snippet_form=snippet_form, snippet_list=snippet_list)
        return render(request, self.template_name, template_context)

    # ----------------------------------------------------------------------
    def post(self, request):
        snippet_form = SnippetForm(data=request.POST, request=request)
        if snippet_form.is_valid():
            request, new_snippet = snippet_form.save()
            return HttpResponseRedirect(new_snippet.get_absolute_url())

        return self._render_response(request, snippet_form)


class SnippetNotFoundError(Exception):
    pass


class SnippetDetailView(View):
    template_name = 'pastebin/snippet_details.html'

    # ----------------------------------------------------------------------
    @method_decorator(check_honeypot)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # ----------------------------------------------------------------------
    def get(self, request, snippet_id):
        # load snippet
        try:
            snippet = self._fetch_snippet(snippet_id)
        except SnippetNotFoundError as exc:
            # 404 response with custom message
            context = dict(message=exc)
            return TemplateResponse(request, 'errors/404.html', context=context, status=404)

        new_snippet_initial = dict(content=snippet.content, lexer=snippet.lexer)
        snippet_form = SnippetForm(initial=new_snippet_initial, request=request)

        snippet_list_ = _get_snippet_list(no_content=True)
        template_context = {
            'snippet_list': snippet_list_,
            'snippet_form': snippet_form,
            'snippet': snippet,
            'lines': range(snippet.get_linecount()),
        }

        return render(request, self.template_name, template_context)

    # ----------------------------------------------------------------------
    def _fetch_snippet(self, snippet_id):
        try:
            snippet = Snippet.objects.get(secret_id=snippet_id)
        except MultipleObjectsReturned as exc:
            raise SnippetNotFoundError(
                _('Multiple snippets exist for this slug. This should never happen.')
            ) from exc
        except ObjectDoesNotExist as exc:
            raise SnippetNotFoundError(
                _('This snippet does not exist anymore. Probably its lifetime is expired.')
            ) from exc
        else:
            return snippet


class SnippetDetailRawView(SnippetDetailView):
    template_name = 'pastebin/snippet_details_raw.html'

    # ----------------------------------------------------------------------
    def get(self, request, snippet_id):
        response = super().get(request, snippet_id)
        # set content type
        response['Content-Type'] = 'text/plain;charset=UTF-8'
        return response


class SnippetDeleteView(View):

    # ----------------------------------------------------------------------
    def get(self, request, snippet_id):
        snippet = get_object_or_404(Snippet, secret_id=snippet_id)
        try:
            snippet_list_ = request.session['snippet_list']
        except KeyError:
            # 403 response with custom message
            return TemplateResponse(
                request,
                'errors/403.html',
                context=dict(message=_('You have no recent snippet list, cookie error?')),
                status=403)
        if snippet.pk not in snippet_list_:
            # 403 response with custom message
            return TemplateResponse(
                request,
                'errors/403.html',
                context=dict(message=_('That is not your snippet!')),
                status=403)

        snippet.delete()
        return HttpResponseRedirect(reverse('snippet_new'))


class LatestSnippetsView(TemplateView):
    template_name = 'pastebin/snippet_list.html'

    # ----------------------------------------------------------------------
    def get_context_data(self, **kwargs):
        snippet_list_ = _get_snippet_list()

        context = super().get_context_data(**kwargs)
        context['snippets_max'] = getattr(settings, 'MAX_SNIPPETS_PER_USER', 10)
        context['snippet_list'] = snippet_list_
        return context


class SnippetAPIView(View):

    # ----------------------------------------------------------------------
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # ----------------------------------------------------------------------
    def post(self, request):
        try:
            controller = CreateSnippetApiController(request)
            snippet = controller.create()
        except SnippetValidationError as exc:
            return HttpResponseBadRequest(str(exc), content_type='text/plain')

        site = self._get_site(request)
        absolute_url = snippet.get_absolute_url()
        result = f'https://{site.domain}{absolute_url}'
        return HttpResponse(result, content_type='text/plain')

    # ----------------------------------------------------------------------
    def _get_site(self, request):
        if hasattr(request, 'site'):
            return request.site

        return Site.objects.get_current()
