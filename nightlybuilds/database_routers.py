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

# pylint: disable=protected-access,unused-argument


class NightlyBuildsRouter:
    """
    A router to control all database operations on models in the
    nightlybuilds application.
    """
    # ----------------------------------------------------------------------
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to nightlybuilds.
        """
        if model._meta.app_label == 'nightlybuilds':
            return 'nightlybuilds'
        return None

    # ----------------------------------------------------------------------
    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to nightlybuilds.
        """
        if model._meta.app_label == 'nightlybuilds':
            return 'nightlybuilds'
        return None

    # ----------------------------------------------------------------------
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'nightlybuilds' and \
                obj2._meta.app_label == 'nightlybuilds':
            return True
        return None

    # ----------------------------------------------------------------------
    def allow_migrate(self, database, app_label, model_name=None, **hints):
        return (database != 'nightlybuilds' and app_label != 'nightlybuilds') \
            or (database == 'nightlybuilds' and app_label == 'nightlybuilds')
