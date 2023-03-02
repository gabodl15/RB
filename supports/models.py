from django.db import models
from django.contrib.auth.models import User
from clients.models import Client, Profile
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

class Install(models.Model):
    inspect = models.OneToOneField(Inspect, on_delete=models.CASCADE)
    realized = models.CharField(max_length=3, choices=CHOICES, default=NOT)

    def __str__(self):
        return self.inspect.inspect.client.name

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

class Support(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    support = models.TextField()
    realized = models.CharField(max_length=3, choices=CHOICES, default=NOT)

    def __str__(self):
        return self.client.name

class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    message = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class WirelessSupportSheet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    support = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    sheet = models.CharField(max_length=100)
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.client.name

class FiberSupportSheet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    support = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    sheet = models.CharField(max_length=100)
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.client.name

class WirelessInstallationSheet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    installation = models.OneToOneField(Install, null=True, on_delete=models.SET_NULL)
    sheet = models.CharField(max_length=100)
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.client.name

class FiberInstallationSheet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    installation = models.OneToOneField(Install, null=True, on_delete=models.SET_NULL)
    sheet = models.CharField(max_length=100)
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.client.name
class WirelessInspectionSheet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    inspection = models.OneToOneField(Inspect, on_delete=models.CASCADE)
    sheet = models.CharField(max_length=100)
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.client.name

class FiberInspectionSheet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    inspection = models.OneToOneField(Inspect, on_delete=models.CASCADE)
    sheet = models.CharField(max_length=100)
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.client.name
