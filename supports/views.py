from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Inspect, Material, Install, Log
from .forms import FeasibleOrNotFeasibleForm, MaterialFiberForm, MaterialWirelessForm
from clients.models import Client
from ventas.models import Inspection, FeasibleOrNotFeasible as VentasFeasibleOrNotFeasible

# Create your views here.
def index(request):
    missing_inspect = Inspect.objects.filter(realized='NOT')
    missing_install = Install.objects.filter(realized='NOT')
    context = {
        'missing_inspect': missing_inspect,
        'missing_install': missing_install,
    }
    return render(request, 'supports/index.html', context)

def show(request, id):
    installation = Install.objects.get(id=id)
    client = installation.inspect.inspect.client
    material = installation.inspect.material
    context = {
        'installation': installation,
        'client': client,
        'material':material
    }
    return render(request, 'supports/show.html', context)

def updateInspection(request, id):
    support_inspection = Inspect.objects.get(id=id)
    if request.method == 'POST':
        """ VALIDAMOS QUE EL FOR SEA VALIDO """
        form_feasible = FeasibleOrNotFeasibleForm(request.POST)

        if form_feasible.is_valid():
            """ OBTENEMOS EL OBJECTO SIN GUARDARLO """
            support_feasible = form_feasible.save(commit=False)
            
            """ EN EL CASO DE QUE SEA FACTIBLE """
            if 'NOT' not in support_feasible.feasible:
                material = MaterialFiberForm(request.POST) if support_inspection.inspect.inspection_type == "OF" else MaterialWirelessForm(request.POST)
                if material.is_valid():
                    """ CREAR LISTA DE MATERIALES """
                    material.save()
                else:
                    messages.error(request, 'FORMULARIO DE MATERIALES NO VALIDO')
                    return redirect('supports.inspection.update', id=id)
            """ GUARDO EL OBJECTO UNA VEZ VERIFICADO AMBOS FORMUARIOS """
            support_feasible.save()
            
            ventas_inspection = Inspection.objects.get(id=support_inspection.inspect_id)
            ventas_inspection.inspection = 'YES'
            ventas_inspection.save()

            """ INSPECCION REALIZADA """
            support_inspection.realized = 'YES'
            support_inspection.save()
            """ REGISTRANDO EN EL LOG QUE SE REALIZÓ LA INSPECCION """
            support_log = Log(
                            user=request.user,
                            action='Inspección Realizada',
                            message='La inspección para el cliente {} fue realizada'.format(support_inspection)
                            )
            support_log.save()

            """ FACTIBLE O NO EN VENTAS """
            ventas_feasible = VentasFeasibleOrNotFeasible()
            ventas_feasible.inspection = ventas_inspection
            ventas_feasible.feasible = support_feasible.feasible
            ventas_feasible.comment = support_feasible.comment
            ventas_feasible.save()
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