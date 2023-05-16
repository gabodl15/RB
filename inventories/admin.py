from django.contrib import admin
from .models import Brand, Inventory

# Register your models here.
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Brand, BrandAdmin)

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'description', 'stored')
    search_fields = ('name', 'brand__name', 'description')

admin.site.register(Inventory, InventoryAdmin)