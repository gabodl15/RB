from django.shortcuts import render
from routers.models import Router
from clients.models import Client

def index(request):
    get_clients = Client.objects.all()
    clients = len(get_clients)
    get_routers = Router.objects.all()
    routers = len(get_routers)

    context = {
        'clients': clients,
        'routers': routers,
    }
    return render(request, 'index.html', context)
