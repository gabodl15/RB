from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Client
from .forms import ClientForm

class ClientCreateView(CreateView):
    model = Client
    fields = '__all__'
    template_name = 'clients/create.html'
    success_url = '/clients'

def index(request):
    clients = Client.objects.all()
    return render(request, 'clients/index.html', {'clients': clients})

def show(request, id):
    client = Client.objects.get(id=id)
    return render(request, 'clients/show.html', {'client': client})