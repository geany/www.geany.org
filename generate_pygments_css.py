#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from pygments.formatters import HtmlFormatter


f = open('pastebin/static/css/pygments.css', 'w')

# You can change style and the html class here:
f.write(HtmlFormatter(style='colorful').get_style_defs('.code'))

f.close()
