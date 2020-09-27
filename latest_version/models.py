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

from django.db import models


class LatestVersion(models.Model):

    name = models.CharField(max_length=50, unique=True)
    version = models.CharField(max_length=50, verbose_name='Latest Geany version')
    release_date = models.DateTimeField()
    github_link = models.CharField(
        max_length=255,
        verbose_name='Link to the Commits page on Github (everything after '
                     'https://github.com/geany/geany/)')

    class Meta:
        verbose_name = 'Latest Version'
        verbose_name_plural = 'Latest Version'

    # ----------------------------------------------------------------------
    def delete(self, using=None, keep_parents=False):
        """Never delete anything"""

    # ----------------------------------------------------------------------
    def __str__(self):
        return '{} {}'.format(self.name, self.version)
