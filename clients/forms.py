from django.forms import ModelForm
from .models import Client, Profile

class ClientForm(ModelForm):
    class Meta:
        model = Client
        exclude = ('created_at',)

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('client', 'created', 'updated',)
