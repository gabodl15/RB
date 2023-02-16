from django.db import models
from django.contrib.auth.models import User
from clients.models import Client, Profile

# Create your models here.
class Payment(models.Model):
    PA = 'payment'
    CR = 'credit'
    CHOICES = [
        (PA, 'Pago de Mensualidad'),
        (CR, 'Abono')
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    operation = models.CharField(max_length=20, verbose_name='Operación', choices=CHOICES)
    transaction = models.CharField(max_length=10, verbose_name='Transacción')
    dolars = models.FloatField(null=True, blank=True, verbose_name='Dolares')
    bolivares = models.FloatField(null=True, blank=True, verbose_name='Bolivares')
    bank = models.CharField(max_length=40, null=True, blank=True, verbose_name='Banco')
    rate = models.FloatField(null=True, blank=True, verbose_name='Tasa')
    transaction_reference = models.IntegerField(null=True, blank=True, verbose_name='Referencia de Transacción')
    comment = models.TextField(null=True, blank=True, verbose_name='Comentario')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client.name

class Debt(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.FloatField()
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client.name

class NotSuspend(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.profile.name

class AdministrationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    message = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name