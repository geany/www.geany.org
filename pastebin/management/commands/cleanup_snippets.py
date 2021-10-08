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

import sys

from django.core.management.base import BaseCommand
from django.utils import timezone

from pastebin.models import Snippet


class Command(BaseCommand):

    help = 'Purges snippets that are expired'

    # ----------------------------------------------------------------------
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run', '-d',
            action='store_true',
            dest='dry_run',
            help='Don\'t do anything.')

    # ----------------------------------------------------------------------
    def handle(self, *args, **options):
        deleteable_snippets = Snippet.objects.filter(expires__lte=timezone.now())
        sys.stdout.write(f'{deleteable_snippets.count()} snippets gets deleted:\n')
        for deleteable_snippet in deleteable_snippets:
            sys.stdout.write(
                f'- {deleteable_snippet.secret_id} ({deleteable_snippet.expires})\n')
        if options.get('dry_run'):
            sys.stdout.write('Dry run - Doing nothing! *crossingfingers*\n')
        else:
            deleteable_snippets.delete()
