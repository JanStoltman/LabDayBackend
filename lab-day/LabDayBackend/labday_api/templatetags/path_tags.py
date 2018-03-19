from django import template
from ..models import Path

register = template.Library()

@register.simple_tag
def get_paths():
    return Path.objects.all()