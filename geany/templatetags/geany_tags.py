# -*- coding: utf-8 -*-

from django import template

register = template.Library()


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
