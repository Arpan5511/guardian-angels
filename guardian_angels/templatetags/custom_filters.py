from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def has_attribute(obj, attr):
    """Check if an object has a specific attribute"""
    return hasattr(obj, attr)

@register.filter
def add_class(field, css_class):
    """Add CSS classes to form fields"""
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={'class': css_class})
    return field

