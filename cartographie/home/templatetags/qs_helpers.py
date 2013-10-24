from django import template 

register = template.Library()


@register.simple_tag
def qs_replace(value, **kwargs):
    new_qs = value.copy()
    for k in kwargs:
        new_qs[k] = kwargs[k]
    return new_qs.urlencode()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
