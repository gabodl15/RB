from django.contrib import admin
from .models import Nodo, CompanyAntenna
from django import forms
# Register your models here.
admin.site.register(Nodo)

class CompanyAntennaAdminForm(forms.ModelForm):
    class Meta:
        model = CompanyAntenna
        widgets = {
            'password': forms.TextInput
        }
        fields = '__all__'

class CompanyAntennaAdmin(admin.ModelAdmin):
    form = CompanyAntennaAdminForm

admin.site.register(CompanyAntenna, CompanyAntennaAdmin)
