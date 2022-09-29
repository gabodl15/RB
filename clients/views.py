from django.shortcuts import render
from .models import Client
from .forms import ClientForm
def index(request):
    clients = Client.objects.all()
    return render(request, 'clients/index.html', {'clients': clients})

def create(request):
    form = ClientForm
    return render(request, 'clients/create.html', {'form': form})

def show(request, id):
    client = Client.objects.get(id=id)
    return render(request, 'clients/show.html', {'client': client})