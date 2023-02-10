from django.contrib import admin, messages
from django.urls import reverse
from django.shortcuts import redirect
from routers.functions import Connection
from .models import Client, Profile
from django import forms

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'dni', 'phone', 'email')
    search_fields = ('name', 'last_name', 'dni')
    ordering = ('name',)

admin.site.register(Client, ClientAdmin)

class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        widgets = {
            'password': forms.TextInput
        }
        fields = '__all__'
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'password', 'router', 'plan', 'cutoff_date', 'agreement')
    search_fields = ('client__name', 'name', 'router__name', 'plan__name')

    form = ProfileAdminForm

    def delete_model(self, request, obj):
        # INTENTAMOS ELIMINAR EL PERFIL DEL MIKROTIK PREVIO A ELIMINARLO DE LA BASE DE DATOS.
        connection = Connection(obj.router)
        if connection.active is False:
            self.message_user(request, connection.message, level=messages.ERROR)
        return redirect('admin:clients_profile_change', obj.id)
            
admin.site.register(Profile, ProfileAdmin)
