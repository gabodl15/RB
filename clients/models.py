from django.db import models
from routers.models import Router, Plan
from fernet_fields import EncryptedTextField

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    address = models.TextField()
    coordinates = models.CharField(max_length=100, default=None, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    name = models.CharField(max_length=30)
    password = EncryptedTextField()
    mac = models.CharField(max_length=20, null=True, blank=True)
    # cutoff_date
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    router = models.ForeignKey(Router, on_delete=models.RESTRICT)
    plan = models.ForeignKey(Plan, on_delete=models.RESTRICT)
    agreement = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    def __str__(self):
        return self.name
    
