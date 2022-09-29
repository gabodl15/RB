from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name