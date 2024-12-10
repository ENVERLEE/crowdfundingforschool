from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def div(value, arg):
    try:
        value = Decimal(str(value))
        arg = Decimal(str(arg))
        if arg == 0:
            return 0
        return value / arg
    except:
        return 0

@register.filter
def mul(value, arg):
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except:
        return 0
