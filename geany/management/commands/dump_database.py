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

from json import dump, load
from os import unlink

from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand, call_command
from django.db.models import F

from nightlybuilds.models import NightlyBuild


class Command(BaseCommand):
    help = "Dump the database (excluding users, sessions and logs)"

    # ----------------------------------------------------------------------
    def handle(self, *args, **options):
        self._dump_main_database()
        self._remove_sensitive_information_from_dump()
        self._dump_nightly_builds_database()

    # ----------------------------------------------------------------------
    def _dump_main_database(self):
        print('Dump main database')
        call_command(
            'dumpdata',
            '--exclude', 'auth.user',
            '--exclude', 'sessions.session',
            '--exclude', 'admin.logentry',
            '--exclude', 'pastebin.snippet',
            '--exclude', 'mezzanine_sync_pages.mezzaninesyncpages',
            '--indent', '2',
            '--output', 'database.json')

    # ----------------------------------------------------------------------
    def _remove_sensitive_information_from_dump(self):
        # remove potential sensitive information
        with open('database.json', encoding='utf-8') as data_input:
            data = load(data_input)
            for record in data:
                model = record['model']
                name = record['fields'].get('name')

                if model == 'conf.setting' and name == 'COMMENTS_NOTIFICATION_EMAILS':
                    record['fields']['value'] = 'root@localhost'
                if model == 'news.newspost':
                    # replace user foreign key as we do not export any users but will create
                    # a default user with pk 1 below
                    record['fields']['user'] = 1

            # add a default user
            user = {
                'model': 'auth.user',
                'pk': 1,
                'fields': {
                    'password': make_password('change-me'),
                    'last_login': '2019-12-20T23:42:00Z',  # :)
                    'is_superuser': True,
                    'username': 'admin',
                    'first_name': 'Qui-Gon',
                    'last_name': 'Jinn',
                    'email': 'root@localhost',
                    'is_staff': True,
                    'is_active': True,
                    'date_joined': '1977-05-25T23:42:00Z',
                    'groups': [],
                    'user_permissions': []
                }
            }
            data.append(user)

        # write data back to the database file
        with open('database.json', 'w', encoding='utf-8') as output:
            dump(data, output, indent=2)

    # ----------------------------------------------------------------------
    def _dump_nightly_builds_database(self):
        # query the last nightly build for each build target for the dump
        # (dumping all builds would be too large)
        queryset = NightlyBuild.objects.\
            prefetch_related('nightly_build_target').\
            filter(nightly_build_target__last_nightly_build_id=F('nightly_build_id')).\
            order_by('nightly_build_target__project', 'nightly_build_target__identifier')
        pks = [str(item.nightly_build_id) for item in queryset]

        database_nightlybuilds_filename = 'tmp_database_nightlybuilds.json'
        database_nightlybuild_targets_filename = 'tmp_database_nightlybuild_targets.json'
        print('Dump nightlybuilds.NightlyBuild')
        call_command(
            'dumpdata',
            '--database', 'nightlybuilds',
            '--pks', ','.join(pks),
            '--indent', '2',
            '--output', database_nightlybuilds_filename,
            'nightlybuilds.NightlyBuild')

        print('Dump nightlybuilds.NightlyBuildTarget')
        call_command(
            'dumpdata',
            '--database', 'nightlybuilds',
            '--indent', '2',
            '--output', database_nightlybuild_targets_filename,
            'nightlybuilds.NightlyBuildTarget')

        # merge the nightly build dump files
        filenames = (database_nightlybuilds_filename, database_nightlybuild_targets_filename)
        records = []
        with open('database_nightlybuilds.json', 'w', encoding='utf-8') as output:
            for filename in filenames:
                with open(filename, encoding='utf-8') as infile:
                    data = load(infile)
                    records.extend(data)

            dump(records, output, indent=2)

        unlink(database_nightlybuilds_filename)
        unlink(database_nightlybuild_targets_filename)
