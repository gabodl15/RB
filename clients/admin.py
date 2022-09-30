from django.contrib import admin
from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'dni', 'phone', 'email')
    search_fields = ('name', 'last_name', 'dni')
    ordering = ('name',)

admin.site.register(Client, ClientAdmin)
