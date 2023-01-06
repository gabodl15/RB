from django.contrib.auth.models import User
from django.db import models
from clients.models import Client
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
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

class FeasibleOrNotFeasible():
    FA = 'FEASABLE'
    NF = 'NOT FEASABLE'
    CHOICES = [
        (FA, 'FACTIBLE'),
        (NF, 'NO FACTIBLE')
    ]
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE)
    feasible = models.CharField(max_length=10, choices=CHOICES, null=True, blank=True, default=None)