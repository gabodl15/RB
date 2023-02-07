from django.core.exceptions import ObjectDoesNotExist
from logs.models import GlobalLog
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
            self.api=  self.connection.get_api()
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

    def set_query(self, query, id, attr, sentence):
        if attr == 'password':
            self.api.get_resource(query).set(id=id, password=sentence)
        if attr == 'profile':
            self.api.get_resource(query).set(id=id, profile=sentence)

    def remove(self, query, id):
        self.api.get_resource(query).remove(id=id)
        
    def disconnect(self):
        self.connection.disconnect()
