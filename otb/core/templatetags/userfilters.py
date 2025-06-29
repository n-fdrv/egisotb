from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter(name='field_type')
def field_type(field, type):
    return field.as_widget(attrs={'type': type})