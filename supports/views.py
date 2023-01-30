from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from .models import Inspect, Material, Install, Log
from .forms import FeasibleOrNotFeasibleForm, MaterialFiberForm, MaterialWirelessForm
from .sheet_pdf import Pdf
from clients.models import Client
from ventas.models import Inspection, FeasibleOrNotFeasible as VentasFeasibleOrNotFeasible

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

import io

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

def inspection_show(request, id):
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
    client = support_inspection.inspect.client
    form = FeasibleOrNotFeasibleForm(initial={'inspect': support_inspection})
    material_form = MaterialFiberForm(initial={'inspect': support_inspection}) if support_inspection.inspect.inspection_type == "OF" else MaterialWirelessForm(initial={'inspect': support_inspection})
    context ={
        'client': client,
        'form': form,
        'inspect': support_inspection,
        'material_form': material_form,
    }
    return render(request, 'supports/inspection_show.html', context)

def support_print(request, support, id):
    if support == 'installations':
        obj = Install.objects.get(id=id)
        client_id = obj.inspect.inspect.client.id
    if support == 'inspections':
        obj = Inspect.objects.get(id=id)
        client_id = obj.inspect.client.id
    client = Client.objects.get(id=client_id)
    media = settings.MEDIA_URL

    sheet = Pdf(obj, client, support)
    saved_sheet = sheet.create_sheet()
    
    support_sheet = media + saved_sheet
    
    data = {
            'support_sheet':support_sheet
    }
    return JsonResponse(data)