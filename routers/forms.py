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

class QueueForm(forms.Form):
    name = forms.CharField(label='Name')
    target = forms.GenericIPAddressField(label='IP')
    destination = forms.GenericIPAddressField(label='dst', required=False)
    upload = forms.CharField(label='Upload')
    download = forms.CharField(label='Download')

class PppForm(forms.Form):
    name = forms.CharField(label='Name')
    password = forms.CharField(label='Password', required=False)
    comment = forms.CharField(label='comment', required=False)
    profile = forms.ChoiceField(label='profiles', widget=forms.Select)