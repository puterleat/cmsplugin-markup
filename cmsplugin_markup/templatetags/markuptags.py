from django import template

register = template.Library()

@register.tag
def rendermarkup(parser, token):
    return RenderMarkupNode()

class RenderMarkupNode(template.Node):
    def render(self, context):
        try:
            return context['object'].render(context)
        except:
            return u''
