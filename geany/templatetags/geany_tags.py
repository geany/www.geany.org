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

import logging

from django import template
from mezzanine.template import Library


register = Library()
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class EvaluateNode(template.Node):
    """As found on http://stackoverflow.com/questions/1278042/in-django-is-there-an-easy-way-to-render-a-text-field-as-a-template-in-a-templ"""  # noqa: E501 pylint: disable=line-too-long

    # ----------------------------------------------------------------------
    def __init__(self, variable, target_var_name):
        self._variable = template.Variable(variable)
        self._target_var_name = target_var_name

    # ----------------------------------------------------------------------
    def render(self, context):
        try:
            content = self._variable.resolve(context)
            content_template = template.Template(content)
            rendered_content = content_template.render(context)
            context[self._target_var_name] = rendered_content
        except (template.VariableDoesNotExist, template.TemplateSyntaxError) as exc:
            return f'Error rendering: {exc}'

        return ''


# ----------------------------------------------------------------------
@register.tag(name='evaluate')
def do_evaluate(parser, token):  # pylint: disable=unused-argument
    """
    tag usage {% evaluate object.textfield %}
    """
    try:
        _, variable, _, target_var_name = token.split_contents()
    except ValueError as exc:
        token_name = token.contents.split()[1]
        raise template.TemplateSyntaxError(
            f'{token_name!r} tag requires a single argument') from exc
    return EvaluateNode(variable, target_var_name)


# ----------------------------------------------------------------------
@register.filter(name='add_css')
def add_css(field, css):
    # read existing CSS classes
    css_classes = field.field.widget.attrs.get('class', '')
    # add new ones
    css_classes = f'{css_classes} {css}'
    # render the widget
    return field.as_widget(attrs={'class': css_classes})
