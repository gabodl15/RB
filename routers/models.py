from django.db import models
from fernet_fields import EncryptedTextField

from nodos.models import Nodo

class Router(models.Model):
    name = models.CharField(max_length=50)
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    user = models.CharField(max_length=100)
    password = EncryptedTextField()
    port = models.IntegerField(default=8728)
    nodo = models.ForeignKey(Nodo, blank=True, null=True, on_delete=models.RESTRICT)
    created = models.DateTimeField(auto_now_add=True)
    #updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    routers = models.ManyToManyField(Router)

    def __str__(self):
        return self.name
