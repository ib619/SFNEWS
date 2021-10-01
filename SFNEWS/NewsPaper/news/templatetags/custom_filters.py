from django import template
import re

register = template.Library()

CENSORED_WORDS = {
    'fuck': '****',
    'shit': '****',
    'cunt': '****',
    'ass': '***',
    'piss': '***',
    'bastard': '*******',
    'dick': '****'
}


@register.filter(name='Censor')
def Censor(value):
    if not isinstance(value, str):
        raise ValueError("Censor function accepts only strings")

    temp = value
    for word in CENSORED_WORDS.keys():
        test = re.compile(re.escape(word), re.IGNORECASE)
        result = test.sub(CENSORED_WORDS[word], temp)
        temp = str(result)
    return temp


