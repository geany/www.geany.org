# -*- coding: utf-8 -*-

from django.template import Library
from pastebin.highlight import pygmentize


register = Library()


#----------------------------------------------------------------------
@register.filter
def in_list(value, arg):
    return value in arg


#----------------------------------------------------------------------
@register.filter
def highlight(snippet, line_count=None):
    h = pygmentize(snippet.content, snippet.lexer)
    if h:
        lines = h.splitlines()
    else:
        lines = snippet.content.splitlines()

    if line_count:
        lines = lines[:line_count]
        lines.append(u'...')
    return lines
