from django import template
import routeros_api

register = template.Library()
@register.filter
def check_profile(profile):
    print(profile.router.ip, profile.router.user, profile.router.password, profile.router.port)
    try:
        connection = routeros_api.RouterOsApiPool(
            profile.router.ip,
            username=profile.router.user,
            password=profile.router.password,
            port=profile.router.port,
            plaintext_login=True,
        )
        api = connection.get_api()
        
    except:
        return 'Error en la conexion'

    active = api.get_resource('/ppp/active').get(name=profile.name)
    connection.disconnect()
    if len(active):
        data = f"<a href='http://{active[0]['address']}' class='green-text' target='_blank'>{active[0]['address']}</a>"
    else:
        data = "<span class='red-text'>No logueado</span>"
    return data