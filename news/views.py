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

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import date, safe
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, View
from mezzanine.core.templatetags.mezzanine_tags import richtext_filters

from news.models import NewsPost


class NewsPostPublishedMixin:

    # ----------------------------------------------------------------------
    def get_queryset(self):
        """ filter non-published news posts except for staff users """
        user = self.request.user
        return NewsPost.objects.\
            published(for_user=user).\
            order_by('-publish_date')


class NewsListView(NewsPostPublishedMixin, ListView):

    model = NewsPost
    template_name = 'news/list.html'


class NewsDetailView(NewsPostPublishedMixin, View):
    template_name = 'news/detail.html'

    # ----------------------------------------------------------------------
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # ----------------------------------------------------------------------
    def get(self, request, newspost_slug):
        newspost = get_object_or_404(NewsPost, slug=newspost_slug)
        return render(request, self.template_name, {'newspost': newspost})

    # ----------------------------------------------------------------------
    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        newspost_slug = request.POST.get('newspost_slug')
        try:
            newspost = NewsPost.objects.get(slug=newspost_slug)
        except NewsPost.DoesNotExist:
            error_message = f'News post item for "{newspost_slug}" could not be found'
            result = {'error': error_message}
        else:
            # adapt to dict
            user_name = newspost.user.get_full_name()
            publish_date = date(newspost.publish_date, 'F dS, Y')
            content = safe(richtext_filters(newspost.content))
            result = {
                'error': None,
                'title': newspost.title,
                'content': content,
                'user': user_name,
                'publish_date': publish_date,
            }

        return JsonResponse(result, safe=True)
