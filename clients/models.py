from django.db import models
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
    
class Inspection(models.Model):
    YES = 'YES'
    NOT = 'NOT'
    DEC = 'DEC' # DECLINED
    CHOICES = [
        (YES, 'SI'),
        (NOT, 'NO'),
        (DEC, 'DECLINÓ')
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    address = models.TextField()
    inspection = models.CharField(max_length=3, choices=CHOICES, default=NOT)
    comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)