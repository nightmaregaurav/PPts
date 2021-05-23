from django import template

register = template.Library()


@register.filter()
def break_table(value1):
    count = value1.count()
    if count <= 10:
        div = count
    else:
        diff = count/2
        if diff == int(diff):
            div = int(diff)
        else:
            div = int(diff) + 1

    value1 = list(value1)
    return [value1[i:i+div] for i in range(0, len(value1), div)]


@register.filter()
def sign(value1):
    if value1<0:
        return '<span style="font-family: sans-serif;">(-</span>' + str(abs(value1)) + \
               '<span style="font-family: sans-serif;">)</span>'
    elif value1 == 0:
        return ''
    else:
        return '<span style="font-family: sans-serif;">(+</span>' + str(abs(value1)) + \
               '<span style="font-family: sans-serif;">)</span>'
