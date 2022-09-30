from django.contrib import admin
from .models import Router

class RouterAdmin(admin.ModelAdmin):
    list_display = ("name","ip",)
    search_fields = ("name", "ip",)
    list_filter = ("name",)
# Register your models here.
admin.site.register(Router, RouterAdmin)