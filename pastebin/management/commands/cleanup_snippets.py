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


from django.core.management.base import LabelCommand
from optparse import make_option
from pastebin.models import Snippet
import datetime
import sys


########################################################################
class Command(LabelCommand):
    option_list = LabelCommand.option_list + (
        make_option('--dry-run', '-d', action='store_true', dest='dry_run',
            help='Don\'t do anything.'),
    )
    help = "Purges snippets that are expired"

    #----------------------------------------------------------------------
    def handle(self, *args, **options):
        deleteable_snippets = Snippet.objects.filter(expires__lte=datetime.datetime.now())
        sys.stdout.write(u"%s snippets gets deleted:\n" % deleteable_snippets.count())
        for d in deleteable_snippets:
            sys.stdout.write(u"- %s (%s)\n" % (d.secret_id, d.expires))
        if options.get('dry_run'):
            sys.stdout.write(u'Dry run - Doing nothing! *crossingfingers*\n')
        else:
            deleteable_snippets.delete()
