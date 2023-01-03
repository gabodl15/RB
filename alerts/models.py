from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Alert(models.Model):
    SL = 'SL' # SOLVED
    AT = 'AT' # ATTENDING
    WT = 'WT' # WAITING
    CHOICES = [
        (SL, 'SOLVENTADO'),
        (AT, 'ATENDIENDO'),
        (WT, 'EN ESPERA')
    ]
    alert = models.CharField(max_length=50)
    message = models.TextField()
    status = models.CharField(max_length=2, choices=CHOICES, default=WT)
    attended_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    color = models.CharField(max_length=15, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.alert
