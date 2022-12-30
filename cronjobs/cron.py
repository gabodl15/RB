import importlib.util, os, sys
from pathlib import Path


def check_if_a_package_is_installed(list_of_packages):
    BASE_DIR = Path(__file__).resolve().parent
    packages_not_installed = "{}/{}".format(BASE_DIR, 'packages_not_installed.txt')
    if os.path.exists(packages_not_installed):
        os.remove(packages_not_installed)
    for package_name in list_of_packages:
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            with open(packages_not_installed, 'a') as f:
                f.write('{} is no installed!\n'.format(package_name))
                f.close
    if os.path.exists(packages_not_installed):
        return False
    else:
        return True

def router_connection():
    list_of_packages = [
        'routeros_api',
        'paramiko',
    ]
    if check_if_a_package_is_installed(list_of_packages):
        from routers.models import Router
        import routeros_api, paramiko
        try:
            connection = routeros_api.RouterOsApiPool(
                '192.168.99.1',
                username='Gabriel',
                password='pretoriano',
                port=8728,
                plaintext_login=True,
            )
            api = connection.get_api()
            add_ppp = api.get_resource('/ppp/secret')
            add_ppp.add(
                name='gabrielito',
                service='pppoe',
                password='19945978',
                profile='default',
            )

            # TERMINAR CONEXION
            connection.disconnect()
        except e:
            pass


def index():
    if check_if_a_package_is_installed(['routeros_api',]):
        print('HOLA')
    else:
        print('CHAO')
