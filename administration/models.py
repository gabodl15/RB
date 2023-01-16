from django.db import models
from django.contrib.auth.models import User
from clients.models import Client, Profile

# Create your models here.
class Payment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    operation = models.CharField(max_length=20)
    transaction = models.CharField(max_length=10)
    dolars = models.FloatField(null=True, blank=True)
    bolivares = models.FloatField(null=True, blank=True)
    bank = models.CharField(max_length=40, null=True, blank=True)
    rate = models.FloatField(null=True, blank=True)
    transaction_reference = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Debt(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.FloatField()
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class NotSuspend(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class AdministrationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    message = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)