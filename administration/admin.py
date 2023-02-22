from django.contrib import admin
from .models import Payment, AdministrationLog
# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('client', 'operation', 'dolars', 'bolivares', 'created')
    search_fields = ('client__name', 'created')
    class Meta:
        ordering = ['client','lower']

admin.site.register(Payment, PaymentAdmin)

class AdministrationLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'message', 'created')

admin.site.register(AdministrationLog, AdministrationLogAdmin)