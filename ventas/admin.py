from django.contrib import admin
from .models import Inspection, Referred, FeasibleOrNotFeasible

# Register your models here.
class InspectionAdmin(admin.ModelAdmin):
    list_display = ('client','inspection', 'address', 'inspection_type')

admin.site.register(Inspection, InspectionAdmin)

class ReferredAdmin(admin.ModelAdmin):
    list_display = ('referred', 'client')

admin.site.register(Referred, ReferredAdmin)

class FeasibleOrNotFeasibleAdmin(admin.ModelAdmin):
    list_display = ['inspection', 'feasible']

admin.site.register(FeasibleOrNotFeasible, FeasibleOrNotFeasibleAdmin)