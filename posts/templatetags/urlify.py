from django import template
from urllib import parse
register=template.Library()
@register.filter
def urlify(value):
    return parse.quote(value)