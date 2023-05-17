from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='users', null=True, blank=True)
    messages = models.BooleanField(default=False, verbose_name='Enviar Mensajes')

    def __str__(self):
        return self.user.username
