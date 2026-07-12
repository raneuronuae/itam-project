from django import template
from num2words import num2words

register = template.Library()

@register.filter
def to_words(value):
    try:
        # দশমিকের পর ২ ঘর পর্যন্ত কথায় রূপান্তর করবে
        return num2words(float(value), to='currency', currency='USD').replace('dollars', '').replace('cents', '').strip().capitalize()
    except:
        return value