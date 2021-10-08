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

from django.db import models


class NightlyBuildTarget(models.Model):

    nightly_build_target_id = models.PositiveIntegerField(primary_key=True)
    active = models.BooleanField()
    project = models.CharField(max_length=50)
    identifier = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    arch = models.CharField(max_length=50)
    folder = models.CharField(max_length=50)
    last_nightly_build = models.ForeignKey(
        'NightlyBuild',
        null=True,
        blank=True,
        on_delete=models.PROTECT)

    class Meta:
        ordering = ('name', 'arch')
        db_table = 'nightly_build_target'

    # ----------------------------------------------------------------------
    def __str__(self):
        return f'{self.name} {self.arch}'


class NightlyBuild(models.Model):

    nightly_build_id = models.PositiveIntegerField(primary_key=True)
    nightly_build_target = models.ForeignKey('NightlyBuildTarget', on_delete=models.PROTECT)
    status = models.BooleanField()
    revision = models.CharField(max_length=255)
    compiler_version = models.CharField(max_length=50)
    glib_version = models.CharField(max_length=50)
    gtk_version = models.CharField(max_length=50)
    log_stdout = models.CharField(max_length=100, blank=True, null=True)
    log_stderr = models.CharField(max_length=100, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    build_host = models.CharField(max_length=255)
    build_date = models.DateTimeField(max_length=255)

    class Meta:
        ordering = ('-build_date',)
        db_table = 'nightly_build'

    # ----------------------------------------------------------------------
    def get_status(self):
        return not self.status

    # ----------------------------------------------------------------------
    def get_status_text(self):
        if self.get_status():
            return 'Built successfully'

        return 'Build failed, see the logs for details'

    # ----------------------------------------------------------------------
    def __str__(self):
        return f'{self.build_date} {self.nightly_build_target}'
