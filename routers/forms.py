from django.forms import ModelForm
from .models import Router
from django import forms

class RouterForm(ModelForm):
    class Meta:
        model = Router
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
        }

routers = Router.objects.all()
CHOICES = [('0', 'TODOS LOS ROUTERS')]
for router in routers:
    CHOICES.append((router.id, router.name))

class QueueForm(forms.Form):

    router = forms.ChoiceField(label='In', choices=CHOICES, widget=forms.Select)
    name = forms.CharField(label='Name')
    target = forms.GenericIPAddressField(label='IP')
    destination = forms.GenericIPAddressField(label='dst',required=False)
    upload = forms.CharField(label='Upload')
    download = forms.CharField(label='Download')
