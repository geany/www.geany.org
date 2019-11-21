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

import os

from django import template
from django.conf import settings
from django.utils.html import format_html


register = template.Library()
BASE_DIR = settings.NIGHTLYBUILDS_BASE_DIR


# ----------------------------------------------------------------------
@register.simple_tag
def get_build_log(nightly_build, log_type):
    if log_type == 'Stdout':
        log = nightly_build.log_stdout
    else:
        log = nightly_build.log_stderr

    if log:
        logfile_path = os.path.join(BASE_DIR, nightly_build.nightly_build_target.folder, log)
        try:
            size = os.stat(logfile_path).st_size
        except OSError:
            pass
        else:
            if size > 0:
                return format_html(
                    '<a href="https://nightly.geany.org/{}/{}">{}</stdout>',
                    nightly_build.nightly_build_target.folder,
                    log,
                    log_type)
    return ''


# ----------------------------------------------------------------------
@register.simple_tag
def get_details(nightly_build):
    header_txt = os.path.join(BASE_DIR, nightly_build.nightly_build_target.folder, 'header.html')
    if os.path.exists(header_txt):
        return format_html(
            '<a href="https://nightly.geany.org/{}/">Details</a>',
            nightly_build.nightly_build_target.folder)

    return ''
