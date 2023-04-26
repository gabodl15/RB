from django.db import models
from django.db.models.functions import Concat
from routers.models import Router, Plan
from fernet_fields import EncryptedTextField

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Apellido')
    dni = models.CharField(max_length=20, unique=True, verbose_name='Cedula de Indentidad')
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name='Teléfono')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='Correo Electrónico')
    address = models.TextField(verbose_name='Dirección')
    coordinates = models.CharField(max_length=100, default=None, null=True, blank=True, verbose_name='Coordenadas')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Profile(models.Model):

    OF = 'OF' # OPTICAL FIBER
    WA = 'WA' # WIFI ANTENNA
    CHOICES = [
        (OF, 'Fibra Optica'),
        (WA, 'Antena WiFi')
    ]

    name = models.CharField(max_length=30)
    password = EncryptedTextField()
    mac = models.CharField(max_length=20, null=True, blank=True)
    connection_mode = models.CharField(max_length=2, choices=CHOICES, default=WA)
    cutoff_date = models.DateField(null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    router = models.ForeignKey(Router, on_delete=models.RESTRICT)
    plan = models.ForeignKey(Plan, on_delete=models.RESTRICT)
    agreement = models.BooleanField(default=False, verbose_name='Convenio')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Suspended(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    previus = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    active_cutting = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.profile.name
    
    class Meta:
        ordering = ['profile__name']
    
class Log(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    message = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client.name

class ProfileAlert(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    alert = models.CharField(max_length=200, verbose_name='Alerta')
    solved = models.BooleanField(default=False, verbose_name='Solventado')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)