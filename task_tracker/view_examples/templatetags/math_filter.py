from django import template

register = template.Library()


@register.filter
def modulo(value, arg):
    try:
        return int(value) % int(arg)
    except (ValueError, ZeroDivisionError):
        return None


@register.filter
def multiply(value, arg):
    try:
        return int(value) * int(arg)
    except (ValueError, ZeroDivisionError):
        return None


@register.filter
def power(value, arg):
    try:
        return int(value) ** int(arg)
    except (ValueError, ZeroDivisionError):
        return None
