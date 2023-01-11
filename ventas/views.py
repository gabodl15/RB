from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from clients.forms import ClientForm
from clients.models import Client
from supports.models import Inspect, Material
from .forms import InspectionForm, UpdateInspectionForm
from .models import Inspection, FeasibleOrNotFeasible
import datetime

# Create your views here.
def index(request):
    today = datetime.date.today()
    this_month_inspections = Inspection.objects.filter(created__month=today.month)
    missing_inspect = Inspection.objects.filter(inspection='NOT')
    feasible = FeasibleOrNotFeasible.objects.filter(customer_informed='NOT')
    context ={
        'today': today,
        'this_month_inspections': this_month_inspections,
        'missing_inspect': missing_inspect,
        'feasible': feasible,
    }
    return render(request, 'ventas/index.html', context)

def inspectionResult(request):

    context = {

    }
    return render(request, 'ventas/inspection_result.html', context)

def showInspection(request):
    pass

def addInspection(request, id):
    client = Client.objects.get(id=id)
    address = client.address if len(client.profile_set.all()) == 0 else ''
    coordinate = client.coordinates if len(client.profile_set.all()) == 0 else ''
    if request.method == 'POST':
        form = InspectionForm(request.POST)
        if form.is_valid():
            ventas_inspection = form.save()
            support_inspect = Inspect(inspect=ventas_inspection, realized='NOT')
            support_inspect.save()
            messages.success(request, 'INSPECCION GUARDADA CON EXITO')
            return redirect('clients.show', id=id)
    form = InspectionForm(initial={'client': client, 'address': address, 'coordinates': coordinate})
    context = {
        'client': client,
        'form': form,
    }
    return render(request, 'ventas/add_inspection.html', context)

def updateInspection(request, id):
    inspection = Inspection.objects.get(id=id)
    if request.method == 'POST':
        form = UpdateInspectionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if inspection.inspection != obj.inspection:
                if obj.inspection == 'DEC':
                    if obj.comment != '':
                        obj.save()
                    else:
                        messages.error(request, 'DEBE HABER UN MOTIVO POR EL CUAL DECLINÓ')
        else:
            messages.error(request, 'NO ES CORRECTO EL FORMULARIO')
    form = UpdateInspectionForm(instance=inspection)
    context ={
        'form': form,
        'inspection': inspection
    }
    return render(request, 'ventas/inspection_update.html', context)

def informInspection(request, id):
    feasible = FeasibleOrNotFeasible.objects.get(id=id)
    try:
        from supports.models import Material
        from supports.forms import MaterialFiberForm, MaterialWirelessForm
        m_id = feasible.inspection.inspect.material.id
        obj = Material.objects.get(id=m_id).__dict__
        materials_filter = [
            '_state',
            'id',
            'inspect_id'
        ]
        material = {}
        for el, val in obj.items():
            if el not in materials_filter:
                material[el] = val
    except :
        material = None
    
    context = {
        'feasible': feasible,
        'material': material,
    }
    return render(request, 'ventas/inspection_inform.html', context)