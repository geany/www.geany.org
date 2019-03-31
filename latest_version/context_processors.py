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

from geany.decorators import cache_function, CACHE_TIMEOUT_1HOUR
from latest_version.models import LatestVersion


# ----------------------------------------------------------------------
@cache_function(CACHE_TIMEOUT_1HOUR, ignore_arguments=True)
def latest_version(request):
    geany_latest_version = LatestVersion.objects.get(id=1)
    return dict(geany_latest_version=geany_latest_version)
