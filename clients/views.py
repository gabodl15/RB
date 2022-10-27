from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Client
from .forms import ClientForm
import folium

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
    coordinates = client.coordinates
    if coordinates:
        x = coordinates.split(',')
        map = folium.Map(location=[float(x[0]), float(x[1])], zoom_start=16)
        folium.Marker([float(x[0]), float(x[1])], tooltip='Clip aqui').add_to(map)
        map_render = map.get_root().render()
    else:
        map_render = None
    context = {
        'client': client,
        'map_render': map_render,
    }
    return render(request, 'clients/show.html', context)