import ast
from django import template

register = template.Library()


# noinspection PyBroadException
@register.simple_tag
def var(value):
    try:
        ret = ast.literal_eval(value)
    except Exception:
        try:
            ret = ast.literal_eval("\'" + value + "\'")
        except Exception:
            ret = value
    return ret


@register.simple_tag
def assign(value):
    return value


@register.filter()
def concat(value1, value2):
    return str(value1) + str(value2)
