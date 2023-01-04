from django.contrib import admin
from .models import Alert

# Register your models here.
class AlertAdmin(admin.ModelAdmin):
    admin.site.register(Alert)