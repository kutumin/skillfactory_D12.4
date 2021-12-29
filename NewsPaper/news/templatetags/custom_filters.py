from django import template
import re

blacklist = ['bitch', 'whore','whore!!!']
 
register = template.Library()

@register.filter(name='multiply')

def multiply(value, arg):
    return str(value) * arg 

@register.filter(name='Censor')

def Censor(value):
    w=value.split()
    for i in range(len(w)):
        if w[i] in blacklist:
            w[i] ='!!цензура!!'
    string = ' '.join([str(item) for item in w])
    return string
