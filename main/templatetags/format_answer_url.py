from django import template

register = template.Library()

@register.filter
def format_answer_url(value):
    return 'answer/' + str(value)
    #return value.replace("&","and")