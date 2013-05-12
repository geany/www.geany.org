# -*- coding: utf-8 -*-

from django.db.models import F
from django.views.generic import ListView
from nightlybuilds.models import NightlyBuild


########################################################################
class NightlyBuildsView(ListView):
    template_name = "nightlybuilds.html"

    context_object_name = 'nightlybuilds'

    queryset = NightlyBuild.objects.\
                prefetch_related('nightly_build_target').\
                filter(nightly_build_target__last_nightly_build_id=F('nightly_build_id')).\
                order_by('nightly_build_target__project', 'nightly_build_target__identifier')
