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
from django.core.management import BaseCommand

from static_docs.generate_i18n_statistics import TranslationStatisticsGenerator


class Command(BaseCommand):
    help = "Generate a JSON file with I18N statistics after updating PO files"

    # ----------------------------------------------------------------------
    def handle(self, *args, **options):
        generator = TranslationStatisticsGenerator(
            'geany',
            settings.STATIC_DOCS_GEANY_SOURCE_TARBALL,
            settings.STATIC_DOCS_GEANY_DESTINATION_DIR,
            settings.STATIC_DOCS_GEANY_I18N_STATISTICS_FILENAME,
        )
        generator.generate()
