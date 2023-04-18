from django import template
from routers.views import Connection

register = template.Library()
@register.filter
def check_plan(profile):
    conn = Connection(profile.router)
    if conn.active:
        active = conn.name_query('/ppp/secret', profile.name)
        conn.disconnect()
        if len(active):
            if active[0]['profile'] != profile.plan.name:
                return f"<span class='red-text'>{profile.plan.name}</span>"
    return profile.plan.name