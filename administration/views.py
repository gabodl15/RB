from django.shortcuts import render, redirect
from django.contrib import messages
from clients.models import Client, Profile
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from .models import Payment, NotSuspend, AdministrationLog
# Create your views here.

# OBTENEMOS EL DIA EN EL QUE ESTAMOS, PARA FILTRAR EL COBRO.
# ESTABLECEMOS UN MAXIMO DE 5 DIAS DE LA FECHA DE CORTE DEL CLIENTE
collection = date.today()
td = timedelta(5)

def _log(request, action, message):
    log = AdministrationLog(
        user=request.user,
        action=action,
        message=message
    )
    log.save()
    return None

def index(request):
    profiles_from_database = Profile.objects.all().order_by('client__name')
    filter_profile_in_list = []

    # RECORREMOS EL OBJETO PROFILE
    # DE EXISTIR UN PERFIL CUYA FECHA DE CORTE ESTE DENTRO DE 5 DIAS CON LA FECHA ACTUAL, LO AGREGAMOS A LA LISTA
    for profile in profiles_from_database:
        if abs(collection - profile.cutoff_date) <= td:
            filter_profile_in_list.append(profile)

    context = {
        'profiles': filter_profile_in_list
    }


    return render(request, 'administration/index.html', context)

def payment(request, id):
    client = Client.objects.get(id=id)
    if request.method == 'POST':
        operation = request.POST['operation']
        profiles_id = request.POST.getlist('profiles[]')
        transaction = request.POST['transaction']
        dolars = request.POST['dolars'] # CAN BE NULL
        bolivares = request.POST['bolivares'] # CAN BE NULL
        bank = request.POST['bank'] # CAN BE NULL
        rate = request.POST['rate'] # CAN BE NULL
        transaction_reference = request.POST['transaction_reference'] # CAN BE NULL
        comment = request.POST['comment'] # CAN BE NULL
        
        if not profiles_id:
            messages.error(request, 'NO HA SELECCIONADO UN PERFIL')
            return redirect(request.META.get('HTTP_REFERER'))

        if operation == 'not_suspend':
            for p in profiles_id:
                profile = Profile.objects.get(id=p)
                not_suspend = NotSuspend(
                    profile = profile,
                    date = profile.cutoff_date
                )
                not_suspend.save()
            if len(profiles_id) == 1:
                message = 'El usuario no será suspendido'
            else:
                message = 'Los usuarios no serán suspendidos'
            messages.success(request, message)
            return redirect('administrations.index')
            
        if operation == 'payment':
            for p in profiles_id:
                profile = Profile.objects.get(id=p)
                profile.cutoff_date = profile.cutoff_date + relativedelta(months=1)
                profile.save()

        payment = Payment(
            client = client,
            operation = operation,
            transaction = transaction,
            dolars = dolars,
            bolivares = bolivares,
            bank = bank,
            rate = rate,
            transaction_reference = transaction_reference,
            comment = comment,
        )
        _log(request, 'payment record', 'Se ha registrado el pago del Cliente {}'.format(client))
        return redirect('administrations.index')

    profiles = Profile.objects.filter(client_id=client)
    
    context = {
        'client': client,
        'profiles': profiles,
    }
    return render(request, 'administration/client/payment.html', context)