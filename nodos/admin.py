from django.contrib import admin
from .models import Nodo, CompanyAntenna
from django import forms
# Register your models here.

class NodoAdmin(admin.ModelAdmin):
    def map(self, coordinates):
        print('It have set coordinates')
    def save_model(self, request, obj, form, change):
        if change == 0 and request.POST['coordinates']:
            self.map(request.POST['coordinates'])
        if change:
            if obj.coordinates != request.POST['coordinates']:
                self.map(request.POST['coordinates'])
        super().save_model(request, obj, form, change)

admin.site.register(Nodo, NodoAdmin)

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
