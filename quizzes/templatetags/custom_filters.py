from django import template

register = template.Library()

@register.filter(name='get_option')
def get_option(question, option_num):
    option_field = f"option_{option_num}"
    return getattr(question, option_field, None)