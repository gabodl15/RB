from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models.functions import TruncMonth
from django.db.models import Count
from clients.forms import ClientForm
from clients.models import Client, Profile
from supports.models import Inspect, Material, Install
from logs.models import GlobalLog
from .forms import InspectionForm, UpdateInspectionForm, InstallationFeeForm
from .models import Inspection, FeasibleOrNotFeasible, Installation, InstallationFee, VentaLog
import datetime


# CREATE GENERAL FUNCTIONS HERE
def logs(user, action, message):
    log = VentaLog(
        user=user,
        action=action,
        message=message
    )
    log.save()

# Create your views here.
def index(request):
    today = datetime.date.today()
    this_month_inspections = Inspection.objects.filter(created__month=today.month)
    missing_inspect = Inspection.objects.filter(inspection='NOT').order_by('-id')
    feasible = FeasibleOrNotFeasible.objects.filter(customer_informed='NOT').order_by('-id')
    installation = Installation.objects.filter(payment='NOT').order_by('-id')

    _ = Profile.objects.annotate(month=TruncMonth('created')).values('month').annotate(c=Count('id')).values('month', 'c')
    months = []
    records = []
    for p in _:
        months.append(p['month'].strftime('%B'))
        records.append(p['c'])

    profile_registration_chart = {'months': months, 'records': records}

    context ={
        'today': today,
        'this_month_inspections': this_month_inspections,
        'missing_inspect': missing_inspect,
        'feasible': feasible,
        'installation': installation,
        'graph': profile_registration_chart
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
            logs(request.user, 'Add Inspection', 'Se ha generado la inspección para el cliente {}'.format(client))
            global_log = GlobalLog(
                user = request.user,
                action = 'Add Inspection',
                message = 'Se ha generado la inspección para el cliente {}'.format(client)
            )
            global_log.save()
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
                        support_inspection = Inspect.objects.get(id=inspection.inspect.id)
                        support_inspection.delete()
                        inspection.inspection = 'DEC'
                        inspection.save()
                        logs(
                            request.user, 
                            'Update Inspection', 
                            'Se ha cancelado la inspección de {} en {}'.format(inspection, inspection.address)
                        )
                        global_log = GlobalLog(
                            request.user, 
                            'Update Inspection', 
                            'Se ha cancelado la inspección de {} en {}'.format(inspection, inspection.address)
                        )
                        global_log.save()
                    else:
                        messages.error(request, 'DEBE HABER UN MOTIVO POR EL CUAL DECLINÓ')
                    return redirect('ventas.index')
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
        inspection_type = feasible.inspection.inspection_type
        obj = Material.objects.get(id=m_id)
        material = MaterialWirelessForm(instance=obj) if inspection_type == 'WA' else MaterialFiberForm(instance=obj)
    except :
        material = None
    
    context = {
        'feasible': feasible,
        'material': material,
    }
    return render(request, 'ventas/inspection_inform.html', context)

def informedInspection(request):
    f_id = request.POST['feasible_id']
    feasible = FeasibleOrNotFeasible.objects.get(id=f_id)
    feasible.customer_informed = 'YES'
    if hasattr(feasible.inspection.inspect, 'material'):
        material = Material.objects.get(id=feasible.inspection.inspect.material.id)
    else:
        material = None

    if 'NOT' not in feasible.feasible:
        installation = Installation(
            inspection=feasible.inspection,
            material=material,
        )
        installation.save()
    
    feasible.save()

    logs(
        request.user, 
        'Inform Inspection',
        'Cliente {} ha sido informado sobre su inspección'.format(feasible)
    )
    global_log = GlobalLog(
        request.user, 
        'Inform Inspection',
        'Cliente {} ha sido informado sobre su inspección'.format(feasible)
    )
    global_log.save()
    

    return redirect('ventas.index')

def updateInstallation(request, id):
    installation = Installation.objects.get(id=id)
    if request.method == 'POST':
        i_fee = InstallationFeeForm(request.POST)
        if i_fee.is_valid():
            installation.payment = 'YES'
            installation.save()
            obj = i_fee.save()
            
            """ CREAMOS LA INSTALACION PARA SOPORTE """
            support_inspect = obj.installation.inspection.inspect

            support_instalation = Install(
                inspect=support_inspect
            )
            support_instalation.save()
            return redirect('ventas.index')
        else:
            messages.error(request,'FORMULARIO NO VALIDO')
    form = InstallationFeeForm(initial={'installation': installation})
    context = {
        'installation': installation,
        'form': form
    }
    return render(request, 'ventas/installation_update.html', context)