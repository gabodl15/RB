from django.contrib.auth.models import User
from django.db import models
from clients.models import Client
from django import forms
# Create your models here.
class Inspection(models.Model):

    OF = 'OF' # OPTICAL FIBER
    WA = 'WA' # WIFI ANTENNA
    YES = 'YES'
    NOT = 'NOT'
    DEC = 'DEC' # DECLINED

    CHOICES = [
        (OF, 'Fibra Optica'),
        (WA, 'Antena WiFi')
    ]
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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client.name

class Referred(models.Model):
    referred = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.client.name

class FeasibleOrNotFeasible(models.Model):
    YES = 'YES'
    NOT = 'NOT'
    CHOICES = [
        (YES, 'SI'),
        (NOT, 'NO'),
    ]
    FA = 'FEASIBLE'
    NF = 'NOT FEASIBLE'
    FEASIABLE_CHOICES = [
        (FA, 'FACTIBLE'),
        (NF, 'NO FACTIBLE')
    ]
    inspection = models.OneToOneField(Inspection, on_delete=models.CASCADE)
    customer_informed = models.CharField(max_length=3, choices=CHOICES, default=NOT)
    feasible = models.CharField(max_length=15, choices=FEASIABLE_CHOICES)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.inspection.client.name

class Installation(models.Model):
    YES = 'YES'
    NOT = 'NOT'
    DEC = 'DEC' # DECLINED
    CHOICES = [
        (YES, 'SI'),
        (NOT, 'NO'),
        (DEC, 'DECLINÓ')
    ]
    inspection = models.OneToOneField(Inspection, on_delete=models.CASCADE)
    material = models.OneToOneField('supports.Material', on_delete=models.CASCADE, null=True)
    payment = models.CharField(max_length=3, choices=CHOICES, default=NOT)
    amount = models.IntegerField(null=True, blank=True, default=None)

    def __str__(self):
        return self.inspection.client.name

class InstallationFee(models.Model):
    BS = 'BS'
    DS = 'DS'
    CURRENCY_CHOICES=[
        (BS, 'BOLIVARES'),
        (DS, 'DOLARES')
    ]
    installation = models.OneToOneField(Installation, on_delete=models.CASCADE)
    installation_fee = models.FloatField()
    currency = models.CharField(max_length=2, choices=CURRENCY_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.installation.inspection.client.name

class VentaLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    message = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)