# -*- coding: utf-8 -*-


########################################################################
class NightlyBuildsRouter(object):
    """
    A router to control all database operations on models in the
    nightlybuilds application.
    """
    #----------------------------------------------------------------------
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to nightlybuilds.
        """
        if model._meta.app_label == 'nightlybuilds':
            return 'nightlybuilds'
        return None

    #----------------------------------------------------------------------
    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to nightlybuilds.
        """
        if model._meta.app_label == 'nightlybuilds':
            return 'nightlybuilds'
        return None

    #----------------------------------------------------------------------
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'nightlybuilds' and \
                obj2._meta.app_label == 'nightlybuilds':
            return True
        return None

    #----------------------------------------------------------------------
    def allow_syncdb(self, db, model):
        return False
