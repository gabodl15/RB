from django.core.exceptions import ObjectDoesNotExist
import routeros_api

class Connection:
    
    def __init__(self, router):
        self.active = False
        try:
            self.connection = routeros_api.RouterOsApiPool(
                router.ip,
                username=router.user,
                password=router.password,
                port=router.port,
                plaintext_login=True,
            )
            self.api = self.connection.get_api()
            self.active = True

        except ObjectDoesNotExist:
            self.message = 'ROUTER NO REGISTRADO'
        except routeros_api.exceptions.RouterOsApiCommunicationError:
            self.message = 'USUARIO O CLAVE INCORRECTOS'
        except routeros_api.exceptions.RouterOsApiConnectionError:
            self.message = 'NO PUDO CONECTAR CON EL ROUTER'
    
    def query(self, query):
        _query = self.api.get_resource(query)
        get_query = _query.get()
        return get_query
    
    def name_query(self, query, name):
        _query = self.api.get_resource(query).get(name=name)
        return _query

    def disconnect(self):
        self.connection.disconnect()

class Profile:
    
    def __init__(self, profile=None):
        self.profile = profile

    def create(self):
        pass

    def update(self, request):
        pass