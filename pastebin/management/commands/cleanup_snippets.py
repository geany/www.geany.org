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

from optparse import make_option
import datetime
import sys

from django.core.management.base import LabelCommand

from pastebin.models import Snippet


class Command(LabelCommand):
    option_list = LabelCommand.option_list + (
        make_option(
            '--dry-run', '-d',
            action='store_true',
            dest='dry_run',
            help='Don\'t do anything.'),
    )
    help = 'Purges snippets that are expired'

    # ----------------------------------------------------------------------
    def handle(self, *args, **options):
        deleteable_snippets = Snippet.objects.filter(expires__lte=datetime.datetime.now())
        sys.stdout.write('{} snippets gets deleted:\n'.format(deleteable_snippets.count()))
        for deleteable_snippet in deleteable_snippets:
            sys.stdout.write(
                u'- {} ({})\n'.format(deleteable_snippet.secret_id, deleteable_snippet.expires))
        if options.get('dry_run'):
            sys.stdout.write('Dry run - Doing nothing! *crossingfingers*\n')
        else:
            deleteable_snippets.delete()
