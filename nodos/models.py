from django.db import models
from fernet_fields import EncryptedTextField

class State(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Nodo(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Estado')
    address = models.CharField(max_length=250, verbose_name='Dirección')
    coordinates = models.CharField(max_length=30, null=True, blank=True, verbose_name='Coordenadas')
    comment = models.TextField(null=True, blank=True, verbose_name='Comentario')

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
    name = models.CharField(max_length=50, verbose_name='Nombre')
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    wireless_mode = models.CharField(max_length=2, choices=CHOICES, default=AP)
    point_to_point = models.BooleanField(default=0, verbose_name='Punto-a-Punto')
    frequency = models.IntegerField(verbose_name='Frecuencia')
    username = models.CharField(max_length=30, default='ubnt')
    password = EncryptedTextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class ClientAntenna(models.Model):
    nodo = models.ForeignKey(Nodo, on_delete=models.SET_NULL, null=True)
    ap = models.ForeignKey(CompanyAntenna, on_delete=models.SET_NULL, null=True)
    profile = models.OneToOneField('clients.Profile', on_delete=models.CASCADE, null=True, verbose_name='ppp')
    user = models.CharField(max_length=20, default='ubnt')
    password = EncryptedTextField()
    brand = models.CharField(max_length=20, default='Ubiquiti', verbose_name='Marca')
    model = models.CharField(max_length=20, verbose_name='Modelo')
    firmware = models.CharField(max_length=40)

    def __str__(self):
        return self.profile.name
    
class CompanyAntennaAlert(models.Model):
    ap = models.ForeignKey(CompanyAntenna, on_delete=models.CASCADE)
    alert = models.CharField(max_length=200)
    solved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class ClientAntennaAlert(models.Model):
    ap = models.ForeignKey(CompanyAntenna, on_delete=models.CASCADE)
    profile = models.ForeignKey('clients.profile', on_delete=models.CASCADE, null=True)
    alert = models.CharField(max_length=200)
    solved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)