from django.shortcuts import render, redirect
from django.contrib import messages
from clients.models import Client, Profile
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from .models import Payment, NotSuspend, AdministrationLog
from logs.models import GlobalLog
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
def _global_log(request, action, message):
    log = GlobalLog(
        user=request.user,
        action=action,
        message=message
    )
    log.save()
    return None

def index(request):
    today = date.today()
    year = today.year
    month = today.month
    
    not_suspend = NotSuspend.objects.filter(date__gte=today.replace(day=1))

    if today.day in range(10, 20):
        search_day = today.replace(day=15)
        profiles = Profile.objects.filter(cutoff_date=search_day).exclude(name__in=[name for name in not_suspend]).order_by('client__name')

    if today.day in range(25, 31) or today.day in range(1, 5):
        if today.day >= 25:
            last_day = monthrange(year, month)[1]
            search_day = today.replace(day=last_day)
        else:
            last_day = monthrange(year, (month - 1))
            search_day = today.replace(day=last_day)
        
        profiles = Profile.objects.filter(cutoff_date=search_day).exclude(name__in=[name for name in not_suspend]).order_by('client__name')

    context = {
        'profiles': profiles
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
                message = 'El usuario del cliente {} no será suspendido'.format(client)
            else:
                message = 'Los usuarios del cliente no serán suspendidos'.format(client)
            messages.success(request, message)
            _log(request, 'Do Not Suspend', 'El/Los usuario(s) del cliente {} no será(n) suspendido(s)'.format(client))
            _global_log(request, 'Do Not Suspend', 'El/Los usuario(s) del cliente {} no será(n) suspendido(s)'.format(client))
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
        _global_log(request, 'payment record', 'Se ha registrado el pago del Cliente {}'.format(client))
        return redirect('administrations.index')

    profiles = Profile.objects.filter(client_id=client)
    
    context = {
        'client': client,
        'profiles': profiles,
    }
    return render(request, 'administration/client/payment.html', context)


def do_not_suspend(request):
    cutoff_date = date.today()
    not_suspend = NotSuspend.objects.filter(date__gt=cutoff_date)
    context = {
        'not_suspend': not_suspend,
    }
    return render(request, 'administration/client/do_not_suspend.html', context)