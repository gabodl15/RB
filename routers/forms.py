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
