from django.shortcuts import render
from clients.models import Client, Profile
from datetime import date, timedelta

# Create your views here.

# OBTENEMOS EL DIA EN EL QUE ESTAMOS, PARA FILTRAR EL COBRO.
# ESTABLECEMOS UN MAXIMO DE 5 DIAS DE LA FECHA DE CORTE DEL CLIENTE
collection = date.today()
td = timedelta(5)

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
    if request.method == 'POST':
        operation = request.POST['operation']
        profiles_id = request.POST['profiles[]']
        transaction = request.POST['transaction']
        dolars = reqeuest.POST['dolars'] # CAN BE NULL
        bolivares = request.POST['bolivares'] # CAN BE NULL
        bank = request.POST['bank'] # CAN BE NULL
        rate = request.POST['rate'] # CAN BE NULL
        transaction_reference = request.POST['transaction_reference'] # CAN BE NULL

    client = Client.objects.get(id=id)
    profiles = Profile.objects.filter(client_id=client)
    
    context = {
        'client': client,
        'profiles': profiles,
    }
    return render(request, 'administration/client/payment.html', context)