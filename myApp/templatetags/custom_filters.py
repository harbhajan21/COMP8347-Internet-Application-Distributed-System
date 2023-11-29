from django import template

register = template.Library()

@register.filter(name='custom_get_value')
def custom_get_value(dictionary, key):
    return dictionary.get(key, '')
