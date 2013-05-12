# coding: utf-8

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
