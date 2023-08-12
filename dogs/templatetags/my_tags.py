from django import template


register = template.Library()


@register.filter
def my_media_filter(val):
    return f'/media/{val}'


@register.simple_tag
def my_media_tag(val):
    return f'/media/{val}'


