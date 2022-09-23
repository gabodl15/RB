from django.db import models

class Router(models.Model):
    name = models.CharField(max_length=50)
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    port = models.IntegerField(default=8728)

    def __str__(self):
        return self.name
