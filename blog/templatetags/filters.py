from django import template
import random

register = template.Library()


@register.filter
def not_in(value, given_list):
    return False if str(value) in given_list else True


@register.filter
def minus_one(value):
    return value-1


@register.filter
def colorize_class(values):
    colors = [
    "primary",
    "secondary",
    "success",
    "danger",
    "warning",
    "info",
    "light",
    "dark"
]
    return colors[random.randint(0, len(colors)-1)]
