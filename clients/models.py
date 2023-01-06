from django.contrib.auth.models import User
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


OF = 'OF' # OPTICAL FIBER
WA = 'WA' # WIFI ANTENNA
CHOICES = [
    (OF, 'Fibra Optica'),
    (WA, 'Antena WiFi')
]
class Profile(models.Model):

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
    INSPECTION_CHOICES = [
        (YES, 'SI'),
        (NOT, 'NO'),
        (DEC, 'DECLINÓ')
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    address = models.TextField()
    inspection_type = models.CharField(max_length=2, choices=CHOICES, default=WA)
    inspection = models.CharField(max_length=3, choices=INSPECTION_CHOICES, default=NOT)
    coordinates = models.CharField(max_length=100, default=None, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    registered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client.name