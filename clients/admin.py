from django.contrib import admin, messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from routers.functions import Connection
from .models import Client, Profile, Suspended
from django import forms

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'dni', 'phone', 'email', 'address')
    search_fields = ('name', 'last_name', 'dni', 'email', 'address')
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
            url = reverse('admin:clients_profile_change', args=[obj.id])
            messages.error(request, 'No se pudo eliminar el objeto.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        router_profile = connection.name_query('/ppp/secret', obj.name)
        if router_profile:
            connection.remove('/ppp/secret', router_profile[0]['id'])
            obj.delete()
        else:
            messages.error(request, 'El usuario no se encuentra en el mikrotik')
    
            
admin.site.register(Profile, ProfileAdmin)

class SuspendedAdmin(admin.ModelAdmin):
    list_display = ('profile', 'previus', 'active_cutting', 'created', 'updated')
    search_fields = ('profile__name', 'previus__name', 'active_cutting', 'created', 'updated')
    
admin.site.register(Suspended, SuspendedAdmin)