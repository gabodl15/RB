from django.contrib import admin
from .models import Inspect, FeasibleOrNotFeasible, Material, Install, WirelessInstallationSheet, Support
from ventas.models import Inspection

# Register your models here.
class FeasibleOrNotFeasibleInLine(admin.StackedInline):
    model = FeasibleOrNotFeasible

class InspectAdmin(admin.ModelAdmin):
    model = Inspect
    list_display = ['inspect','inspection_type','inspection']
    inlines = [FeasibleOrNotFeasibleInLine]

    def inspection(self, obj):
        return obj.inspect.address
    def inspection_type(self, obj):
        return obj.inspect.inspection_type

admin.site.register(Inspect, InspectAdmin)

class MaterialAdmin(admin.ModelAdmin):
    model = Material
    list_display = (
        'inspect',
        'cabling',
        'intallation_location',
        'pipe',
        'wire',
        'base',
        'anchor',
        'welding',
        'tensors',
        'cable_routin',
        'support_post',
        'nap_code',
        'comment',
    )

admin.site.register(Material, MaterialAdmin)

class WirelessInstallationSheetInLine(admin.StackedInline):
    model = WirelessInstallationSheet

class InstallAdmin(admin.ModelAdmin):
    model = Install
    list_display = ['inspect', 'realized']
    inlines = [WirelessInstallationSheetInLine]

admin.site.register(Install, InstallAdmin)

class SupportAdmin(admin.ModelAdmin):
    model = Support
    list_display = ['client', 'profile', 'support', 'realized']

admin.site.register(Support, SupportAdmin)