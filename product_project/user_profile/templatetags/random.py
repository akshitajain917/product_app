import random
from django import template

register = template.Library()

# use to generate random numbers to login
@register.simple_tag
def random_int(a,b=None):
    if b is None:
        a,b = 0,a
    return random.randint(a,b)