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

from django.core.management.base import BaseCommand
from pygments.formatters.html import HtmlFormatter


class Command(BaseCommand):
    help = "Regenerate CSS for snippet sxntax highlighting py Pygments"
    requires_system_checks = False

    # ----------------------------------------------------------------------
    def handle(self, *args, **options):
        with open('pastebin/static/css/pygments.css', 'w', encoding='utf-8') as css_file:
            # You can change style and the html class here:
            css_file.write(HtmlFormatter(style='colorful').get_style_defs('.highlight'))
