from django.shortcuts import render
from routers.models import Router
from clients.models import Client
from nodos.models import Nodo, CompanyAntenna

def index(request):
    clients = len(Client.objects.all())
    routers = len(Router.objects.all())
    nodos = len(Nodo.objects.all())
    antennas = len(CompanyAntenna.objects.all())
    context = {
        'clients': clients,
        'routers': routers,
        'nodos': nodos,
        'antennas': antennas,
    }
    return render(request, 'index.html', context)
