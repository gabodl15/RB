from django.db import models
from clients.models import Client
from users.models import User

# Create your models here.
class TextMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

class ClientMessage(models.Model):
    client = models.ManyToManyField(Client, on_delete=models.CASCADE)
    text_message = models.ForeignKey(TextMessage, on_delete=models.CASCADE)

    def __str__(self):
        return self.client