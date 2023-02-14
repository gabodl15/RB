from django.contrib import admin
from .models import Payment
# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('client', 'operation', 'dolars', 'bolivares', 'created')
    search_fields = ('client', 'created')
    class Meta:
        ordering = ['client','lower']

admin.site.register(Payment, PaymentAdmin)