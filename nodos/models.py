from django.db import models
from fernet_fields import EncryptedTextField
class Nodo(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    coordinates = models.CharField(max_length=30, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class CompanyAntenna(models.Model):
    AP = 'AP'
    STATION = 'ST'
    CHOICES = [
        (AP, 'Access Point'),
        (STATION, 'Station')
    ]

    nodo = models.ForeignKey(Nodo, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    wireless_mode = models.CharField(max_length=2, choices=CHOICES, default=AP)
    point_to_point = models.BooleanField(default=0)
    frequency = models.IntegerField()
    username = models.CharField(max_length=30, default='ubnt')
    password = EncryptedTextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class ClientAntenna(models.Model):
    nodo = models.ForeignKey(Nodo, on_delete=models.SET_NULL, null=True)
    profile = models.ForeignKey('clients.Profile', on_delete=models.CASCADE, null=True)
    user = models.CharField(max_length=20, default='ubnt')
    password = EncryptedTextField()
    brand = models.CharField(max_length=20, default='Ubiquiti')
    model = models.CharField(max_length=20)
    firmware = models.CharField(max_length=40)