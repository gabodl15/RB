from django.forms import ModelForm
from .models import Client, Profile, Inspection

class ClientForm(ModelForm):
    class Meta:
        model = Client
        exclude = ('created_at',)

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('client', 'created', 'updated',)

class InspectionForm(ModelForm):
    class Meta:
        model = Inspection
        exclude = ('created', 'updated', 'inspection')
        
        