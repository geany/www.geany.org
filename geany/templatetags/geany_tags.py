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

from django import template
from django.conf import settings
from mezzanine.template import Library
import logging

register = Library()
logger = logging.getLogger(__name__)


########################################################################
class EvaluateNode(template.Node):
    """As found on http://stackoverflow.com/questions/1278042/in-django-is-there-an-easy-way-to-render-a-text-field-as-a-template-in-a-templ"""

    #----------------------------------------------------------------------
    def __init__(self, variable, target_var_name):
        self._variable = template.Variable(variable)
        self._target_var_name = target_var_name

    #----------------------------------------------------------------------
    def render(self, context):
        try:
            content = self._variable.resolve(context)
            content_template = template.Template(content)
            rendered_content = content_template.render(context)
            context[self._target_var_name] = rendered_content
        except (template.VariableDoesNotExist, template.TemplateSyntaxError), e:
            return u'Error rendering: %s' % unicode(e)

        return ''


#----------------------------------------------------------------------
@register.tag(name='evaluate')
def do_evaluate(parser, token):
    """
    tag usage {% evaluate object.textfield %}
    """
    try:
        _, variable, _, target_var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(u'%r tag requires a single argument' %
                            token.contents.split()[1])
    return EvaluateNode(variable, target_var_name)


#----------------------------------------------------------------------
@register.as_tag
def get_irc_userlist():
    user_list = list()
    try:
        with open(settings.IRC_USER_LIST_FILE) as file_h:
            user_list = file_h.readlines()
    except IOError, e:
        logger.error(u'An error occurred reading IRC user list: %s', unicode(e), exc_info=True)

    # remove newline characters
    user_list = [username.strip() for username in user_list]
    return sorted(user_list)


#----------------------------------------------------------------------
@register.filter(name='add_css')
def add_css(field, css):
    # read existing CSS classes
    css_classes = field.field.widget.attrs.get('class', u'')
    # add new ones
    css_classes = u'%s %s' % (css_classes, css)
    # render the widget
    return field.as_widget(attrs={'class': css_classes})
