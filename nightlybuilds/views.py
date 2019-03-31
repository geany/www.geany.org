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

from django.db.models import F
from django.views.generic import ListView

from nightlybuilds.models import NightlyBuild


class NightlyBuildsView(ListView):
    template_name = "nightlybuilds.html"

    context_object_name = 'nightlybuilds'

    queryset = NightlyBuild.objects.\
                prefetch_related('nightly_build_target').\
                filter(nightly_build_target__active=1).\
                filter(nightly_build_target__last_nightly_build_id=F('nightly_build_id')).\
                order_by('nightly_build_target__project', 'nightly_build_target__identifier')
