from django import template

register = template.Library()


@register.filter
def format_date(value, format="%Y-%m-%d"):
    """ Formats data """

    return value.strftime(format)
