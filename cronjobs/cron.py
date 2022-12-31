import importlib.util, os, sys
from pathlib import Path
from alerts.models import Alert


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

def alerts_record(alert, message):
    previous_records = Alert.objects.filter(message=message, status__in=['WT', 'AT'])
    if len(previous_records) == 0:
        alert_ = Alert(alert=alert, message=message)
        alert_.save()

def ppp_records():
    list_of_packages = [
        'routeros_api',
    ]

    if check_if_a_package_is_installed(list_of_packages):
        from routers.models import Router
        from clients.models import Profile
        import routeros_api
        routers = Router.objects.all()
        for router in routers:
            try:
                connection = routeros_api.RouterOsApiPool(
                    router.ip,
                    username=router.user,
                    password=router.password,
                    port=router.port,
                    plaintext_login=True,
                )
                api = connection.get_api()
                query = api.get_resource('/ppp/secret')
                users_ppp_in_mikrotik = query.get()
                count_users_ppp_mk = len(users_ppp_in_mikrotik)
                users_ppp_in_datadabe = Profile.objects.filter(router_id=router.id)
                count_users_ppp_db = len(users_ppp_in_datadabe)
                compare_number_of_users = count_users_ppp_db - count_users_ppp_mk
                if compare_number_of_users != 0:
                    largest = 'RB' if count_users_ppp_mk > count_users_ppp_db else 'DB'
                    if largest == 'RB':
                        alerts_record('Incongruencia', 'Hay mas registros en el Mikrotik {} que en la base de datos. {} en total.'.format(router.name, abs(compare_number_of_users)))
                    else:
                        alerts_record('Incongruencia', 'Hay mas registros en la Base de Datos que en el Mikrotik {}. {} en total.'.format(abs(compare_number_of_users), router.name))
                # TERMINAR CONEXION
                connection.disconnect()
            except:
                print('NO CONECTO EL ROUTER {}'.format(router.name))

