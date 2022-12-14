from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Inspect, Material
from .forms import FeasibleOrNotFeasibleForm, MaterialFiberForm, MaterialWirelessForm
from ventas.models import Inspection, FeasibleOrNotFeasible as VentasFeasibleOrNotFeasible

# Create your views here.
def index(request):
    missing_inspect = Inspect.objects.filter(realized='NOT')
    context = {
        'missing_inspect': missing_inspect
    }
    return render(request, 'supports/index.html', context)

def updateInspection(request, id):
    support_inspection = Inspect.objects.get(id=id)
    if request.method == 'POST':
        """ VALIDAMOS QUE EL FOR SEA VALIDO """
        form_feasible = FeasibleOrNotFeasibleForm(request.POST)
        material = MaterialFiberForm(request.POST) if support_inspection.inspect.inspection_type == "OF" else MaterialWirelessForm(request.POST)
        if form_feasible.is_valid() and material.is_valid():
            ventas_inspection = Inspection.objects.get(id=support_inspection.inspect_id)
            ventas_inspection.inspection = 'YES'
            ventas_inspection.save()

            """ INSPECCION REALIZADA """
            support_inspection.realized = 'YES'
            support_inspection.save()

            """ FACTIBLE O NO EN SOPORTE """
            support_feasible = form_feasible.save()

            """ FACTIBLE O NO EN VENTAS """
            ventas_feasible = VentasFeasibleOrNotFeasible()
            ventas_feasible.inspection = ventas_inspection
            ventas_feasible.feasible = support_feasible.feasible
            ventas_feasible.comment = support_feasible.comment
            ventas_feasible.save()

            """ EN EL CASO DE QUE SEA FACTIBLE """
            if 'NOT' not in support_feasible.feasible:
                """ CREAR LISTA DE MATERIALES """
                material.save()
        else:
            messages.error(request, 'FORMULARIO NO VALIDO')
            return redirect('supports.inspection.update', id=id)

        return redirect('supports.index')
    form = FeasibleOrNotFeasibleForm(initial={'inspect': support_inspection})
    material_form = MaterialFiberForm(initial={'inspect': support_inspection}) if support_inspection.inspect.inspection_type == "OF" else MaterialWirelessForm(initial={'inspect': support_inspection})
    context ={
        'form': form,
        'inspect': support_inspection,
        'material_form': material_form,
    }
    return render(request, 'supports/inspection_update.html', context)