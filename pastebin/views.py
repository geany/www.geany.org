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
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, View

from geany.decorators import CACHE_TIMEOUT_24HOURS
from pastebin.api.create import CreateSnippetApiController, SnippetValidationError
from pastebin.models import CACHE_KEY_SNIPPET_LIST_FULL, CACHE_KEY_SNIPPET_LIST_NO_CONTENT, Snippet


# ----------------------------------------------------------------------
def _get_snippet_list(no_content=False):
    base_queryset = Snippet.objects.filter(published__lte=timezone.now())
    if no_content:
        queryset = base_queryset.defer('content', 'content_highlighted')
        cache_key = CACHE_KEY_SNIPPET_LIST_NO_CONTENT
    else:
        queryset = base_queryset.all()
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


class SnippetNotFoundError(Exception):
    pass


class SnippetDetailView(View):
    template_name = 'pastebin/snippet_details.html'

    # ----------------------------------------------------------------------
    def get(self, request, snippet_id):
        # load snippet
        try:
            snippet = self._fetch_snippet(snippet_id)
        except SnippetNotFoundError as exc:
            # 404 response with custom message
            context = {'message': exc}
            return TemplateResponse(request, 'errors/404.html', context=context, status=404)

        snippet_list_ = _get_snippet_list(no_content=True)
        template_context = {
            'snippet_list': snippet_list_,
            'snippet': snippet,
            'lines': range(snippet.get_linecount()),
        }

        return render(request, self.template_name, template_context)

    # ----------------------------------------------------------------------
    def _fetch_snippet(self, snippet_id):
        try:
            snippet = Snippet.objects.get(secret_id=snippet_id, published__lte=timezone.now())
        except MultipleObjectsReturned as exc:
            raise SnippetNotFoundError(
                _('Multiple snippets exist for this slug. This should never happen.')
            ) from exc
        except ObjectDoesNotExist as exc:
            raise SnippetNotFoundError(
                _('This snippet does not exist anymore. Probably its lifetime is expired.')
            ) from exc

        return snippet


class SnippetDetailRawView(SnippetDetailView):
    template_name = 'pastebin/snippet_details_raw.html'

    # ----------------------------------------------------------------------
    def get(self, request, snippet_id):
        response = super().get(request, snippet_id)
        # set content type
        response['Content-Type'] = 'text/plain;charset=UTF-8'
        return response


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
