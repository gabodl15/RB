from django.db import models
from django.db.models.functions import Concat
from routers.models import Router, Plan
from fernet_fields import EncryptedTextField

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    dni = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    address = models.TextField()
    coordinates = models.CharField(max_length=100, default=None, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

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
    agreement = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class WirelessSupportSheet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sheet = models.FileField(upload_to='clients/wireless/support/' + str(client))
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.client.name

class FiberSupportSheet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sheet = models.FileField(upload_to='clients/fiber/support/' + str(client))
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.client.name

class WirelessInstallationSheet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sheet = models.FileField(upload_to='clients/wireless/installation/' + str(client))
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.client.name

class FiberInstallationSheet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sheet = models.FileField(upload_to='clients/fiber/installation/' + str(client))
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.client.name
class WirelessInspectionSheet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sheet = models.FileField(upload_to='clients/wireless/inspection/' + str(client))
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.client.name

class FiberInspectionSheet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sheet = models.FileField(upload_to='clients/fiber/inspection/' + str(client))
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.client.name

class Log(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    message = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client.name