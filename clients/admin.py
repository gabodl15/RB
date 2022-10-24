from django.contrib import admin
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

admin.site.register(Profile, ProfileAdmin)