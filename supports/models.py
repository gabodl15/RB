from django.db import models
from clients.models import Client
from ventas.models import Inspection as VI

# Create your models here.
YES = 'YES'
NOT = 'NOT'
CHOICES = [
    (YES, 'SI'),
    (NOT, 'NO'),
]

class Inspect(models.Model):
    inspect = models.OneToOneField(VI, on_delete=models.CASCADE)
    realized = models.CharField(max_length=3, choices=CHOICES, default=NOT)

    def __str__(self):
        return self.inspect.client.name

class FeasibleOrNotFeasible(models.Model):
    FA = 'FEASIBLE'
    NF = 'NOT FEASIBLE'
    FEASIABLE_CHOICES = [
        (FA, 'FACTIBLE'),
        (NF, 'NO FACTIBLE')
    ]
    inspect = models.OneToOneField(Inspect, on_delete=models.CASCADE)
    feasible = models.CharField(max_length=15, choices=FEASIABLE_CHOICES)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.inspect.inspect.client.name

class Instalation(models.Model):
    inspect = models.OneToOneField(Inspect, on_delete=models.CASCADE)
    realized = models.CharField(max_length=3, choices=CHOICES, default=NOT)

    def __str__(self):
        return self.inspect

class Material(models.Model):
    inspect = models.OneToOneField(Inspect, on_delete=models.CASCADE)
    cabling = models.IntegerField()
    intallation_location = models.TextField()
    pipe = models.CharField(max_length=3, null=True, blank=True)
    wire = models.IntegerField(null=True, blank=True)
    base = models.TextField(null=True, blank=True)
    anchor = models.TextField(null=True, blank=True)
    welding = models.TextField(null=True, blank=True)
    tensors = models.IntegerField(null=True, blank=True)
    cable_routin = models.TextField(null=True, blank=True)
    support_post = models.IntegerField(null=True, blank=True)
    nap_code = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.inspect.inspect.client.name
