from django.contrib import admin
from .models import Inspect, FeasibleOrNotFeasible
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