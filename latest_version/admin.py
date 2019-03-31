# coding: utf-8
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

from django.contrib import admin

from latest_version.models import LatestVersion


class LatestVersionAdmin(admin.ModelAdmin):

    model = LatestVersion

    # ----------------------------------------------------------------------
    def has_add_permission(self, request):
        """A fake model should not be added"""
        return False

    # ----------------------------------------------------------------------
    def has_delete_permission(self, request, obj=None):
        """A fake model should not be added"""
        return False


admin.site.register(LatestVersion, LatestVersionAdmin)
