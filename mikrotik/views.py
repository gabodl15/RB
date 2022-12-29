from django.shortcuts import render
from routers.models import Router
from clients.models import Client, Profile
from nodos.models import Nodo, CompanyAntenna

from django.db.models.functions import TruncMonth
from django.db.models import Count

import folium

def index(request):
    map = folium.Map(location=[11.78701807156271, -70.08361994751114], zoom_start=11)
    nodes = Nodo.objects.all()

    for node in nodes:
        coordinates = node.coordinates
        if coordinates:
            x = coordinates.split(',')
            folium.Marker(
                location=[float(x[0]), float(x[1])],
                tooltip=node.name
            ).add_to(map)
    map_render = map.get_root().render()
    len_clients = len(Client.objects.all())
    len_routers = len(Router.objects.all())
    len_nodos = len(nodes)
    len_antennas = len(CompanyAntenna.objects.all())

    _ = Profile.objects.annotate(month=TruncMonth('created')).values('month').annotate(c=Count('id')).values('month', 'c')
    months = []
    records = []
    for p in _:
        months.append(p['month'].strftime('%B'))
        records.append(p['c'])
    
    profile_registration_chart = {'months': months, 'records': records}

    context = {
        'clients': len_clients,
        'routers': len_routers,
        'nodos': len_nodos,
        'antennas': len_antennas,
        'map': map_render,
        'graph': profile_registration_chart
    }
    return render(request, 'index.html', context)

# def login(request):
#     return render(request, 'auth/login.html', {})
