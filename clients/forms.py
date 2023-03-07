from django.forms import ModelForm, Select
from .models import Client, Profile

class ClientForm(ModelForm):
    class Meta:
        model = Client
        exclude = ('created_at',)

class BrowserDefaultSelect(Select):
    def __init__(self, *args, **kwargs):
        attrs = kwargs.get('attrs', {})
        attrs['class'] = attrs.get('class', '') + 'browser-default'
        kwargs['attrs'] = attrs
        super().__init__(*args, **kwargs)

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('client', 'created', 'updated',)
        widgets = {
            'connection_mode': BrowserDefaultSelect()
        }


        