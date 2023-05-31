from django.contrib import admin
from .models import Router, Plan, Olt

class RouterAdmin(admin.ModelAdmin):
    list_display = ("name","ip",)
    search_fields = ("name", "ip",)
    list_filter = ("name",)
# Register your models here.
admin.site.register(Router, RouterAdmin)

class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'router_display')

    def router_display(self, obj):
        return ", ".join([r.name for r in obj.routers.all()])

admin.site.register(Plan, PlanAdmin)

class OltAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'user', 'password')
    ordering = ('name',)
    search_fields = ('name',)

admin.site.register(Olt, OltAdmin)