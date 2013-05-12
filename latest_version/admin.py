# coding: utf-8

from django.contrib import admin
from latest_version.models import LatestVersion


########################################################################
class LatestVersionAdmin(admin.ModelAdmin):

    model = LatestVersion

    #----------------------------------------------------------------------
    def has_add_permission(self, request):
        """A fake model should not be added"""
        return False

    #----------------------------------------------------------------------
    def has_delete_permission(self, request, obj=None):
        """A fake model should not be added"""
        return False


admin.site.register(LatestVersion, LatestVersionAdmin)
