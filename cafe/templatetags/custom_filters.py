from django import template

print("Custom filters loaded successfully.")
register = template.Library()

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key, None)