from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from clients.forms import ClientForm
from clients.models import Client
from .forms import InspectionForm

# Create your views here.
def index(request):
    context ={

    }
    return render(request, 'ventas/index.html', context)

def addClient(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        print(form.save(commit=False))
    form = ClientForm()
    context = {
        'form': form
    }
    return render(request, 'ventas/add_client.html', context)

def addInspection(request, id):
    client = Client.objects.get(id=id)
    address = client.address if len(client.profile_set.all()) == 0 else ''
    coordinate = client.coordinates if len(client.profile_set.all()) == 0 else ''
    if request.method == 'POST':
        form = InspectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'INSPECCION GUARDADA CON EXITO')
            return redirect('clients.show', id=id)
    form = InspectionForm(initial={'client': client, 'address': address, 'coordinates': coordinate})
    context = {
        'client': client,
        'form': form,
    }
    return render(request, 'ventas/add_inspection.html', context)