from django import template
from routers.views import Connection
import routeros_api

register = template.Library()
@register.filter
def check_profile(profile):
    conn = Connection(profile.router)
    active = conn.name_query('/ppp/active', profile.name)
    conn.disconnect()
    if len(active):
        data = f"<a href='http://{active[0]['address']}' class='green-text' target='_blank'>{active[0]['address']}</a>"
    else:
        data = "<span class='red-text'>No logueado</span>"
    return data