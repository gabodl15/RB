from django.contrib import admin
from .models import State, Nodo, CompanyAntenna, ClientAntenna, CompanyAntennaAlert
from django import forms
# Register your models here.

class StateAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(State, StateAdmin)

class NodoAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'comment')
    search_fields = ('name', 'address')
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
    list_display = ('name', 'nodo', 'ip', 'wireless_mode', 'frequency')
    form = CompanyAntennaAdminForm

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('nodo__name')

admin.site.register(CompanyAntenna, CompanyAntennaAdmin)

class ClientAntennaAdmin(admin.ModelAdmin):
    list_display = ('profile', 'nodo', 'ap', 'brand', 'model', 'firmware')
    search_fields = ('profile__name', 'nodo__name', 'ap__name', 'brand', 'model')

admin.site.register(ClientAntenna, ClientAntennaAdmin)

class CompanyAntennaAlertAdmin(admin.ModelAdmin):
    list_display = ('ap', 'alert', 'solved')
    search_fields = ('ap_name', 'alert')

admin.site.register(CompanyAntennaAlert, CompanyAntennaAlertAdmin)