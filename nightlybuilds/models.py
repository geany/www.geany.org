# -*- coding: utf-8 -*-

from django.db import models


########################################################################
class NightlyBuildTarget(models.Model):

    nightly_build_target_id = models.PositiveIntegerField(primary_key=True)
    project = models.CharField(max_length=50)
    identifier = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    arch = models.CharField(max_length=50)
    folder = models.CharField(max_length=50)
    last_nightly_build = models.ForeignKey('NightlyBuild', null=True, blank=True)

    ########################################################################
    class Meta:
        ordering = ('name', 'arch')
        db_table = 'nightly_build_target'

    #----------------------------------------------------------------------
    def __unicode__(self):
        return '%s %s' % (self.name, self.arch)


########################################################################
class NightlyBuild(models.Model):

    nightly_build_id = models.PositiveIntegerField(primary_key=True)
    nightly_build_target = models.ForeignKey('NightlyBuildTarget')
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

    ########################################################################
    class Meta:
        ordering = ('-build_date',)
        db_table = 'nightly_build'

    #----------------------------------------------------------------------
    def get_status(self):
        return not self.status

    #----------------------------------------------------------------------
    def get_status_text(self):
        if self.get_status():
            return u'Built successfully'
        else:
            return 'Build failed, see the logs for details'

    #----------------------------------------------------------------------
    def __unicode__(self):
        return '%s %s' % (self.build_date, self.nightly_build_target)
