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


########################################################################
class LatestVersion(models.Model):

    version = models.CharField(max_length=50, verbose_name=u'Latest Geany version')
    github_link = models.CharField(max_length=255, verbose_name=u'Link to the Commits page on Github (everything after https://github.com/geany/geany/)')

    ########################################################################
    class Meta:
        verbose_name = u'Latest Version'
        verbose_name_plural = u'Latest Version'

    #----------------------------------------------------------------------
    def save(self):
        """Save but replace the existing row instead of adding a new one"""
        self.id = 1
        models.Model.save(self)

    #----------------------------------------------------------------------
    def delete(self):
        """Never delete anything"""

    #----------------------------------------------------------------------
    def __unicode__(self):
        return self.version
