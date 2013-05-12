# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
import os


register = template.Library()
base_dir = settings.NIGHTLYBUILDS_BASE_DIR


#----------------------------------------------------------------------
@register.simple_tag
def get_build_log(nightly_build, log_type):
    if log_type == u'Stdout':
        log = nightly_build.log_stdout
    else:
        log = nightly_build.log_stderr

    if log:
        logfile_path = os.path.join(base_dir, nightly_build.nightly_build_target.folder, log)
        try:
            size = os.stat(logfile_path).st_size
        except (IOError, OSError):
            pass
        else:
            if size > 0:
                path = u'%s/%s' % (nightly_build.nightly_build_target.folder, log)
                return u'<a href="%s">%s</stdout>' % (path, log_type)
    return u''


#----------------------------------------------------------------------
@register.simple_tag
def get_details(nightly_build):
    header_txt = os.path.join(base_dir, nightly_build.nightly_build_target.folder, 'HEADER.txt')
    if os.path.exists(header_txt):
        return u'<a href="/%s/">Details</a>' % (nightly_build.nightly_build_target.folder)
    else:
        return u''
