from django import template
from django.conf import settings

register = template.Library()


@register.assignment_tag
def is_debug_mode():
    return settings.DEBUG
