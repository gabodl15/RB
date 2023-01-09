from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Inspect
from .forms import FeasibleOrNotFeasibleForm
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
        if form_feasible.is_valid():
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
            ventas_feasible.save()
        else:
            messages.error(request, 'FORMULARIO NO VALIDO')
            return redirect('supports.inspection.update', id=id)

        return redirect('supports.index')
    form = FeasibleOrNotFeasibleForm(initial={'inspect': support_inspection})
    context ={
        'form': form,
        'inspect': support_inspection,
    }
    return render(request, 'supports/inspection_update.html', context)