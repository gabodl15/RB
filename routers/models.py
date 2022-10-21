from django.db import models
from django.utils.timezone import now
from fernet_fields import EncryptedTextField

class Router(models.Model):
    name = models.CharField(max_length=50)
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    user = models.CharField(max_length=100)
    password = EncryptedTextField()
    port = models.IntegerField(default=8728)
    created = models.DateTimeField(default=now)

    def __str__(self):
        return self.name
class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    routers = models.ManyToManyField(Router)

    def __str__(self):
        return self.name