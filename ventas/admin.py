from django.contrib import admin
from .models import Referred

# Register your models here.

class ReferredAdmin(admin.ModelAdmin):
    list_display = ('referred', 'client')

admin.site.register(Referred, ReferredAdmin)