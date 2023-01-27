from django import template
import os
register = template.Library()
@register.filter
def ping(hostname):
    # hostname = hostname
    # response = os.system('ping -c 5 ' + hostname)

    return True

def check_profile(profile):
    
    return True